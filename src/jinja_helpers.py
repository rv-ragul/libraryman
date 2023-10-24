from datetime import date
from src.database import get_db
from src.models import Book, Member


db = get_db()


def book_title(bookID: int):
    book = db.get(Book, bookID)
    assert book is not None
    return book.title


def member_name(memberID: int):
    member = db.get(Member, memberID)
    assert member is not None
    return member.name


def days_since_issued(issued_date: date):
    return (date.today() - issued_date).days

def today():
    return date.today()
