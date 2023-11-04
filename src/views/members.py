from flask import Blueprint, render_template, request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import get_db
from src.models import Member

from .auth import login_required


bp = Blueprint("members", __name__, url_prefix="/members")


@bp.get("/<int:id>")
@login_required
def get_member(id):
    """Get information about a member"""

    db = get_db()
    try:
        stmt = select(Member.name, Member.phone, Member.address).where(Member.id == id)
        res: Member = db.execute(stmt).one()
    except NoResultFound:
        return "Member ID doesn't exist", 450
    return {"name": res.name, "phone": res.phone, "address": res.address}


@bp.get("/")
@login_required
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
            return "Couldn't add member", 450

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
            member.name = name
            member.phone = phone
            member.address = address
            db.commit()
        except AssertionError:
            return "Member does not exist", 450
        except IntegrityError:
            db.rollback()
            return "Couldn't update member", 450

    elif request.method == "GET":
        member = None
        id = request.args.get("id")
        if id:
            member = db.get(Member, id)
    return render_template("members/update.html", member=member)  # type:ignore


@bp.delete("/<int:id>")
@login_required
def remove_member(id):
    """Remove a member from Library database"""

    db = get_db()
    try:
        member = db.get(Member, id)
        assert member is not None
        # Have some dept, so dont remove
        if member.dept != 0:  # type:ignore
            return "Due pending, so not removed", 450
        db.delete(member)
        db.commit()
    except AssertionError:
        return "Member doesn't exist", 450
    except IntegrityError:
        db.rollback()
        return "Couldn't remove member", 450

    return ""
