from flask import Flask

from .database import session
from . import auth


def main(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    app.register_blueprint(auth.bp)

    return app
