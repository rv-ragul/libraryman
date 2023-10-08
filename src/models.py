from typing import Dict

from sqlalchemy import BigInteger, Column, Float, Identity, Integer, String, func
from sqlalchemy.types import TIMESTAMP

from src.database import Base, engine


class User(Base):
    __tablename__ = "users"

    name = Column(String(50), primary_key=True)
    password = Column(String(120), nullable=False)

    def __init__(self, name, password):
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
        self.bookID = book.get("bookID")
        self.title = book.get("title")
        self.authors = book.get("authors")
        self.average_rating = book.get("average_rating")
        self.isbn = book.get("isbn")
        self.isbn13 = book.get("isbn13")
        self.language_code = book.get("language_code")
        self.num_pages = book.get("  num_pages")
        self.ratings_count = book.get("ratings_count")
        self.text_reviews_count = book.get("text_reviews_count")
        self.publication_date = book.get("publication_date")
        self.publisher = book.get("publisher")

    def __repr__(self) -> str:
        return f"<Book {self.title!r}"


class Issued(Base):
    __tablename__ = "issued"

    bookId = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    title = Column(String(80), nullable=False)
    authors = Column(String(80), nullable=False)
    issued_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    return_date = Column(TIMESTAMP(timezone=True))


Base.metadata.create_all(bind=engine)
