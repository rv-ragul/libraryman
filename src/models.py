from typing import Dict

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Identity,
    Integer,
    String,
    func,
)

from src.database import Base, engine


class User(Base):
    __tablename__ = "users"

    name = Column(String(50), primary_key=True)
    password = Column(String(120), nullable=False)

    def __init__(self, name, password) -> None:
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User {self.name!r}>"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(String(20), nullable=False)
    phone = Column(String(12), nullable=False)
    address = Column(String(80), nullable=False)
    dept = Column(Integer, nullable=False, server_default="0")

    def __init__(self, name, phone, address) -> None:
        self.name = name
        self.phone = phone
        self.address = address

    def __repr__(self) -> str:
        return f"<Member {self.id, self.name !r}>"


class Book(Base):
    __tablename__ = "books"

    bookID = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    authors = Column(String(100), nullable=False)
    average_rating = Column(Float, nullable=False)
    isbn = Column(String(10), nullable=False)
    isbn13 = Column(BigInteger, nullable=False)
    language_code = Column(String(10), nullable=False)
    num_pages = Column(Integer, nullable=False)
    ratings_count = Column(Integer, nullable=False)
    text_reviews_count = Column(Integer, nullable=False)
    publication_date = Column(String(10), nullable=False)
    publisher = Column(String(100), nullable=False)

    def __init__(self, book: Dict) -> None:
        self.bookID = book["bookID"]
        self.title = book["title"]
        self.authors = book["authors"]
        self.average_rating = book["average_rating"]
        self.isbn = book["isbn"]
        self.isbn13 = book["isbn13"]
        self.language_code = book["language_code"]
        self.num_pages = book["  num_pages"]
        self.ratings_count = book["ratings_count"]
        self.text_reviews_count = book["text_reviews_count"]
        self.publication_date = book["publication_date"]
        self.publisher = book["publisher"]

    def __repr__(self) -> str:
        return f"<Book {self.title!r}"


class Issued(Base):
    __tablename__ = "issued"

    id = Column(Integer, Identity(always=True), primary_key=True)
    bookID = Column(Integer, ForeignKey(Book.bookID), nullable=False)
    memberID = Column(Integer, ForeignKey(Member.id), nullable=False)
    issued_date = Column(Date, nullable=False, server_default=func.current_date())
    return_date = Column(Date)
    rent_paid = Column(Boolean, nullable=False, server_default="false")

    def __init__(self, bookID, memberID) -> None:
        self.bookID = bookID
        self.memberID = memberID

    def __repr__(self) -> str:
        return f"<Issued book {self.bookID} to {self.memberID}>"


Base.metadata.create_all(bind=engine)
