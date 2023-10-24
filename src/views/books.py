from datetime import date, datetime
from typing import Dict

from flask import Blueprint, json, render_template, request
import httpx
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Book, Issued

from .auth import login_required

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/")
@login_required
def view_books():
    """View books in the Library and search them by author and book name"""

    title = request.args.get("title")
    authors = request.args.get("authors")

    db = get_db()
    stmt = select(Book)

    if title:
        stmt = stmt.where(Book.title.like(f"%{title}%"))
    if authors:
        stmt = stmt.where(Book.authors.like(f"%{authors}%"))

    books = db.scalars(stmt).all()
    return render_template("books/view_books.html", books=books)


@bp.get("/issued")
@login_required
def get_issued_books():
    """Get all the issued books"""

    db = get_db()
    stmt = select(Issued).where(
        or_(Issued.return_date == None, Issued.rent_paid == False)
    )
    print(stmt)
    books = db.scalars(stmt).all()
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
            return "Requested book doesn't exist in the Library", 400
        try:
            db.add(Issued(bookID=bookID, memberID=memberID))
            db.commit()
        except IntegrityError:
            db.rollback()
            return "This book already issued to someone", 400

        return "Book issued successfully!", 200
    elif request.method == "GET":
        id = request.args.get("id")
        book = db.get(Book, id)
    return render_template("books/issue.html", book=book)  # type:ignore


@bp.route("/return", methods=["GET", "POST"])
@login_required
def return_book():
    """Issue a book return"""

    db = get_db()
    if request.method == "POST":
        bookID = request.form["bookID"]
        memberID = request.form["memberID"]
        returnDate = request.form["returnDate"]

        fmt = "%a, %d %b %Y %H:%M:%S %Z"
        returnDate = datetime.strptime(returnDate, fmt)
        returnDate = date(returnDate.year, returnDate.month, returnDate.day)

        try:
            stmt = select(Issued).where(
                and_(Issued.bookID == bookID, Issued.memberID == memberID)
            )
            issued_book = db.scalars(stmt).one_or_none()
            assert issued_book is not None
            issued_book.return_date = returnDate  # type:ignore
            db.commit()
        except IntegrityError:
            db.rollback()
            return "Can't return the book", 450
        except AssertionError:
            return "Book with given ID is not issued", 450

        return "Book returned successfully!"
    elif request.method == "GET":
        id = request.args.get("id")
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

        with httpx.Client() as client:
            res = client.get(
                "https://frappe.io/api/method/frappe-library", params=params
            ).text
            _books: Dict = json.loads(res)
            books = _books.get("message")
            assert books is not None
            db.add_all([Book(book) for book in books])
            db.commit()

    return render_template("books/import.html")
