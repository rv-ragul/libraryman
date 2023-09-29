from sqlalchemy import Column, Integer, String, func
from .database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(String(50), unique=True)
    password = Column(String(120))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User {self.name!r}>"


Base.metadata.create_all(bind=engine)
