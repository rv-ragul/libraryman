from flask import Blueprint, render_template, request, flash
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Member
from .auth import login_required


bp = Blueprint("members", __name__, url_prefix="/members")


@bp.route("/", methods=["GET", "POST"])
def members():
    return render_template("members/view.html")


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_member():
    """Add a member to Library database"""

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        db = get_db()
        try:
            db.add(
                Member(
                    name=name,
                    phone=phone,
                    address=address,
                )
            )
            db.commit()
        except IntegrityError:
            db.rollback()
            flash("Some error")

    return render_template("members/add.html")


@bp.delete("/members/<int:id>")
@login_required
def remove_member(id):
    """Remove a member from Library database"""

    db = get_db()
    try:
        # db.delete
        db.execute(delete(Member).where(Member.id == id))
    except IntegrityError:
        db.rollback()

    return render_template("members/view.html")
