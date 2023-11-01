from datetime import datetime
import os
from dataclasses import dataclass

from flask import Flask, render_template, request, send_from_directory
from sqlalchemy import func, select

from src.jinja_helper import today
from src.database import get_db, init_app
from src.views import auth, books, members
from src.models import Book, Issued, Member


app = Flask(__name__)

app.config.from_pyfile("config.py", silent=True)
init_app(app)


@app.get("/")
@auth.login_required
def index():
    db = get_db()

    @dataclass
    class Status:
        book_with_copies: int = 0
        book_without_copies: int = 0
        issued_books: int = 0
        total_members: int = 0
        members_with_dept: int = 0
        total_dept: int = 0

    def db_execute(stmt):
        return db.execute(stmt).scalar()

    status = Status()
    status.book_with_copies = db_execute(select(func.sum(Book.total)))
    status.book_without_copies = db_execute(select(func.count(Book.bookID)))
    status.issued_books = db_execute(
        select(func.count(Issued.id)).where(Issued.return_date == None)
    )

    status.total_members = db_execute(select(func.count(Member.id)))
    status.members_with_dept = db_execute(
        select(func.count(Member.id)).where(Member.dept > 0)
    )
    status.total_dept = db_execute(select(func.sum(Member.dept)))

    return render_template("index.html", status=status)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        date = request.form["date"]
        date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        print(date)
    return render_template("test.html")


app.jinja_env.globals["today"] = today

app.register_blueprint(auth.bp)
app.register_blueprint(books.bp)
app.register_blueprint(members.bp)
