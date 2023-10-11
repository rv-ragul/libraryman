import os
from datetime import datetime

from flask import Flask, render_template, send_from_directory, request

from src import database
from src.views import auth
from src.views import books


app = Flask(__name__)

app.config.from_pyfile("config.py", silent=True)
database.init_app(app)


@app.get("/")
@auth.login_required
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


app.register_blueprint(auth.bp)
app.register_blueprint(books.bp)
