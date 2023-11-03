from datetime import date, datetime

from flask import Blueprint, render_template, request
import httpx
from sqlalchemy import and_, func, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import get_db
from src.models import Book, Issued, Member

from .auth import login_required

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/<int:id>")
@login_required
def get_books(id):
    """Get information about a book"""

    db = get_db()
    try:
        stmt = select(Book.title, Book.authors).where(Book.bookID == id)
        res: Book = db.execute(stmt).one()
    except NoResultFound:
        return "Book ID doesn't exist", 450
    return {"title": res.title, "authors": res.authors}


@bp.get("/")
@login_required
def view_books():
    """View books in the Library and search them by author and book name"""

    title = request.args.get("title")
    authors = request.args.get("authors")

    db = get_db()
    stmt = (
        select(Book.bookID, Book.title, Book.authors, Book.isbn, Book.publisher)
        .add_columns((Book.total - func.count(Issued.bookID)).label("available"))
        .join(Issued, Issued.bookID == Book.bookID, isouter=True)
        .group_by(Book.bookID)
    )

    if title:
        stmt = stmt.where(Book.title.like(f"%{title}%"))
    if authors:
        stmt = stmt.where(Book.authors.like(f"%{authors}%"))

    books = db.execute(stmt).all()
    return render_template("books/view_books.html", books=books)


@bp.get("/issued")
@login_required
def get_issued_books():
    """Get all the issued books"""

    title = request.args.get("title")
    memberID = request.args.get("memberID")

    db = get_db()
    stmt = (
        select(
            Issued.id,
            Issued.issued_date,
            Issued.return_date,
            Issued.rent_paid,
            (func.current_date() - Issued.issued_date).label("days"),
        )
        .where(or_(Issued.return_date == None, Issued.rent_paid == False))
        .add_columns(Book.bookID, Book.title, Member.id.label("memberID"), Member.name)
        .join(Member)
        .join(Book)
    )

    if title:
        stmt = stmt.where(Book.title.like(f"%{title}%"))
    if memberID:
        stmt = stmt.where(Member.id == memberID)

    books = db.execute(stmt).all()
    return render_template("books/view_issued.html", books=books)


@bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue():
    """Issue a book to a member"""

    db = get_db()
    if request.method == "POST":
        bookID = request.form["bookID"]
        memberID = request.form["memberID"]

        if not db.get(Book, bookID):
            return "Requested book doesn't exist in the Library", 450
        try:
            stmt = select(Issued).where(
                and_(Issued.bookID == bookID, Issued.memberID == memberID)
            )
            already_issued = db.scalars(stmt).one_or_none()
            assert already_issued is None
            db.add(Issued(bookID=bookID, memberID=memberID))
            db.commit()
        except AssertionError:
            return "Only one copy can be issued to a person", 450
        except IntegrityError:
            db.rollback()
            return "Member ID doesn't exist", 450

        return ""
    elif request.method == "GET":
        book = None
        id = request.args.get("id")
        if id:
            book = db.get(Book, id)
    return render_template("books/issue.html", book=book)


@bp.route("/return", methods=["GET", "POST"])
@login_required
def return_book():
    """Issue a book return"""

    db = get_db()
    if request.method == "POST":
        bookID = request.form["bookID"]
        memberID = request.form["memberID"]
        returnDate = request.form["returnDate"]

        paid = request.form.get("paid")

        fmt = "%a, %d %b %Y %H:%M:%S %Z"
        returnDate = datetime.strptime(returnDate, fmt)
        returnDate = date(returnDate.year, returnDate.month, returnDate.day)

        try:
            member = db.get(Member, memberID)
            if member is None:
                return "Member ID doesn't exist", 450

            # update return date
            stmt = select(Issued).where(
                and_(Issued.bookID == bookID, Issued.memberID == memberID)
            )
            issued_book = db.scalars(stmt).one_or_none()
            assert issued_book is not None
            issued_book.return_date = returnDate  # type:ignore

            # update dept
            if not paid:
                member.dept += (date.today() - issued_book.issued_date).days
            else:
                issued_book.rent_paid = True  # type:ignore
            db.commit()
        except IntegrityError:
            db.rollback()
            return "Can't return the book", 450
        except AssertionError:
            db.rollback()
            return f"Book with given ID is not issued to {member.name}", 450

        return ""
    elif request.method == "GET":
        book = None
        id = request.args.get("id")
        if id:
            book = db.get(Issued, id)
    return render_template("books/return.html", book=book)  # type:ignore


@bp.route("/import", methods=["GET", "POST"])
@login_required
def import_books():
    """Import books to Library database using frappe API"""

    if request.method == "POST":
        form = dict(request.form)
        params = {key: value for key, value in form.items() if form.get(key)}
        db = get_db()

        try:
            with httpx.Client() as client:
                res = client.get(
                    "https://frappe.io/api/method/frappe-library", params=params
                ).json()
                books = res.get("message")
                assert books is not None
                for book in books:
                    book["num_pages"] = book.pop("  num_pages")
                    stmt = insert(Book).values(book)
                    insert_stmt = stmt.on_conflict_do_update(
                        constraint="books_pkey",
                        set_=dict(
                            total=stmt.excluded.get("total") + Book.total
                        ),  # type:ignore
                    )
                    db.execute(insert_stmt)
            db.commit()
        except AssertionError:
            return "API error", 450
        except IntegrityError:
            return "Database error", 450
        return str(len(books))
    return render_template("books/import.html")
