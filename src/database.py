import click
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

engine = create_engine("postgresql://r-ragul:ragul2003@localhost:5432/postgres")
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def get_db():
    return session


def close_db(_=None):
    session.remove()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""

    Base.metadata.drop_all(engine)
    print("Reinitialized the database")


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
