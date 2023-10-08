from flask import Blueprint, request
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Member


bp = Blueprint("members", __name__, url_prefix="/members")


def add_member():
    """Add a member to Library database"""

    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]

    try:
        db = get_db()
        db.add(
            Member(
                name=name,
                phone=phone,
                address=address,
            )
        )
        db.commit()
    except IntegrityError:
        return False

    return True


def remove_member(id: int):
    """Remove a member from Library database"""

    try:
        db = get_db()
        db.execute(delete(Member).where(Member.id == id))
    except IntegrityError:
        return False

    return True
