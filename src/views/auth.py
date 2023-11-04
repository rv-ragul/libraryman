# contains the views for `/auth` route

import functools

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import get_db
from src.models import User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")

    if username is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute(select(User).where(User.name == username))
            .scalar_one_or_none()  # username is unique for everyone, ensured in register view
        )


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.post("/update")
def update_password():
    password = request.form["password"]
    db = get_db()
    try:
        user = db.get(User, g.user.name)
        assert user is not None
        user.password = generate_password_hash(password)
        db.commit()
    except AssertionError:
        return "Failed to get logged in user", 450
    except IntegrityError:
        db.rollback()
        return "Failed to update password", 450
    return ""


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["userName"]
        password = request.form["password"]

        try:
            db = get_db()
            db.add(User(username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("auth.login"))
        except IntegrityError:
            return f"User {username} is already registered", 450
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["userName"]
        password = request.form["password"]
        user: User | None = None

        db = get_db()
        try:
            user = db.execute(select(User).where(User.name == username)).scalar_one()
        except NoResultFound:
            return "No user found!", 450

        if not check_password_hash(str(user.password), password):
            return "Incorrect credentials", 450

        session.clear()
        session["username"] = user.name
        return redirect(url_for("index"))
    if request.method == "GET" and session.get("username"):
        return redirect(url_for("index"))
    return render_template("auth/login.html")
