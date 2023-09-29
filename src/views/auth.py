# contains the views for `/auth` route

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from src.models import User
from src.database import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/register")
def register():
    return render_template("auth/register.html")


@bp.get("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.post("/register")
def do_register():
    username = request.form["username"]
    password = request.form["password"]
    error = None

    if not username:
        error = "Username is required"
    if not password:
        error = "password is required"

    if error is None:
        try:
            db = get_db()
            db.add(User(username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("index"))
        except IntegrityError:
            error = f"User {username} is already registered"
    flash(error)
    return render_template("auth/register.html")


@bp.post("/login")
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    if not username:
        error = "Incorrect username"
    db = get_db()
    error = None
    user: User
    try:
        user = db.execute(select(User).where(User.name == username)).scalars().one()
    except NoResultFound:
        error = "No user found!"
        flash(error)
        return render_template("auth/login.html")

    print(user.password)
    print(password)
    print(generate_password_hash(password))
    if not check_password_hash(str(user.password), password):
        error = "Incorrect credentials"

    if error is None:
        session.clear()
        session["username"] = user.name
        return redirect(url_for("index"))
    else:
        flash(error)
    return render_template("auth/login.html")
