from flask import Blueprint, render_template, request
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Member

from .auth import login_required


bp = Blueprint("members", __name__, url_prefix="/members")


@bp.get("/")
def view_members():
    """List the members in the database"""

    members = Member.query.all()
    return render_template("members/view.html", members=members)


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
            db.add(Member(name=name, phone=phone, address=address))
            db.commit()
        except IntegrityError:
            db.rollback()
            return "Some error", 400

    return render_template("members/add.html")


@bp.delete("/<int:id>")
@login_required
def remove_member(id):
    """Remove a member from Library database"""

    db = get_db()
    try:
        member = db.get(Member, id)
        db.delete(member)
        db.commit()
    except IntegrityError:
        print("some error")
        db.rollback()
        return "", 400

    return "", 200
