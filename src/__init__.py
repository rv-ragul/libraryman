from flask import Flask, g, redirect, render_template, session, url_for

from . import database
from .views import auth


app = Flask(__name__)

app.config.from_pyfile("config.py", silent=True)

app.register_blueprint(auth.bp)
database.init_app(app)


    return app
