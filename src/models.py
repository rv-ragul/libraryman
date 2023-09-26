from sqlalchemy import Column, Integer, String, func
from .database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User {self.name!r}>"


Base.metadata.create_all(bind=engine)
