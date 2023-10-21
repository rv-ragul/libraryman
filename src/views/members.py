from flask import Blueprint, render_template, request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Member

from .auth import login_required


bp = Blueprint("members", __name__, url_prefix="/members")


@bp.get("/")
def view_members():
    """List the members in the database"""

    id = request.args.get("id")
    name = request.args.get("name")

    db = get_db()
    stmt = select(Member)

    if id:
        stmt = stmt.where(Member.id == id)
    elif name:
        stmt = stmt.where(Member.name.like(f"%{name}%"))

    members = db.scalars(stmt).all()
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


@bp.route("/update", methods=["GET", "POST"])
@login_required
def update_member():
    """Update a member details in the library database"""

    db = get_db()
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        try:
            member = db.get(Member, id)
            assert member is not None
            member.name = name  # type:ignore
            member.phone = phone  # type:ignore
            member.address = address  # type:ignore
            db.commit()
        except AssertionError:
            return "Member does not exist", 400
        except IntegrityError:
            db.rollback()
            return "some error", 400

    member = None
    if request.method == "GET":
        id = request.args.get("id")
        member = db.get(Member, id)
    return render_template("members/update.html", member=member)


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
