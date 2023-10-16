# Define the application directory
import os
from flask_sqlalchemy import SQLAlchemy
from functionalmodelservice.models import Base
import json


class BaseConfig(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Statement for enabling the development environment
    DEBUG = True
    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/datasets"

    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "SECRETSESSION"

    # Secret key for signing cookies
    SECRET_KEY = b"SECRETKEY"

    if os.environ.get("DAF_CREDENTIALS", None) is not None:
        with open(os.environ.get("DAF_CREDENTIALS"), "r") as f:
            AUTH_TOKEN = json.load(f)["token"]
    else:
        AUTH_TOKEN = ""


config = {
    "development": "functionalmodelservice.config.BaseConfig",
    "testing": "functionalmodelservice.config.BaseConfig",
    "default": "functionalmodelservice.config.BaseConfig",
}


def configure_app(app):
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    # object-based default configuration
    app.config.from_object(config[config_name])
    if os.environ.get("FUNCTIONALMODELSERVICE_SETTINGS", None) is not None:
        app.config.from_envvar("FUNCTIONALMODELSERVICE_SETTINGS")
    else:
        # instance-folders configuration
        app.config.from_pyfile("config.cfg", silent=True)
    db = SQLAlchemy(model_class=Base)
    from .schemas import ma

    db.init_app(app)
    ma.init_app(app)
    return app
