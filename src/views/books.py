from datetime import date, datetime
import json.tool
from typing import Dict

from flask import Blueprint, json, render_template, request
import httpx
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Book, Issued

from .auth import login_required

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/")
@login_required
def view_books():
    """View books in the Library and search them by author and book name"""

    books = Book.query.all()
    return render_template("books/view.html", books=books)


@bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue():
    if request.method == "POST":
        book_id = request.form["book_id"]
        user_name = request.form["user_name"]
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]

        db = get_db()
        if not db.get(Book, book_id):
            return "Requested book doesn't exist in the Library", 400
        try:
            db.add(Issued(book_id, user_name, book_name, book_author))
            db.commit()
        except IntegrityError:
            db.rollback()
            return "This book already issued to someone", 400

        return "Book issued successfully!", 200
    return render_template("books/issue.html")


@bp.route("/return", methods=["GET", "POST"])
@login_required
def return_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        return_date = request.form["return_date"]

        fmt = "%a, %d %b %Y %H:%M:%S %Z"
        return_date = datetime.strptime(return_date, fmt)
        return_date = date(return_date.year, return_date.month, return_date.day)

        db = get_db()
        try:
            issued_book = db.get(Issued, book_id)
            assert issued_book is not None
            issued_book.return_date = return_date
            db.commit()
        except IntegrityError:
            db.rollback()
            return "Can't return the book", 400
        except AssertionError:
            return "Book with given ID is not issued", 400

        return "Book returned successfully!"
    return render_template("books/return.html")


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
