import json.tool
from typing import Dict

from flask import Blueprint, flash, json, render_template, request, url_for
import httpx
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Book, Issued
from auth import login_required

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
        user_name = request.form["username"]
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]
        error = None

        db = get_db()
        try:
            db.add(Issued(book_id, user_name, book_name, book_author))
            db.commit()
        except IntegrityError:
            error = "Some problem occurred"

        if error is None:
            flash("Books database updated successfully")
        else:
            flash(error)
    return render_template("books/issue.html")


@bp.route("/return")
@login_required
def return_book():
    if request.method == "POST":
        pass
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

    return render_template(url_for("books.view_books"))
