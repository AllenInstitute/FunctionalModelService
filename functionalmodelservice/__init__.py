from flask import Flask, jsonify, url_for, redirect, Blueprint
from functionalmodelservice.config import configure_app
from functionalmodelservice.database import Base
from functionalmodelservice.utils import get_instance_folder_path
from functionalmodelservice.admin import setup_admin  # noQA: E402
from functionalmodelservice.api import api_bp

# TODO: implement api
# from functionalmodelservice.api import api_bp  # noQA: E402
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
import logging
from flask_migrate import Migrate

from werkzeug.middleware.proxy_fix import ProxyFix
from middle_auth_client import auth_required

__version__ = "0.0.1"

db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def create_app(test_config=None):
    # Define the Flask Object
    app = Flask(
        __name__,
        instance_path=get_instance_folder_path(),
        instance_relative_config=True,
        static_url_path="/functionalmodel/static",
        static_folder="../static",
    )
    CORS(app, expose_headers="WWW-Authenticate")
    # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)
    # app.wsgi_app = ReverseProxied(app.wsgi_app)
    logging.basicConfig(level=logging.DEBUG)

    apibp = Blueprint("api", __name__, url_prefix="/functionalmodel/api")

    @auth_required
    @apibp.route("/versions")
    def versions():
        return jsonify([2]), 200

    # load configuration (from test_config if passed)
    if test_config is None:
        app = configure_app(app)
    else:
        app.config.update(test_config)

    with app.app_context():
        # app.register_blueprint(views_bp, url_prefix="/functionalmodel")
        api = Api(
            apibp, title="Functional Model Service API", version=__version__, doc="/doc"
        )
        api.add_namespace(api_bp, path="/v1")

        app.register_blueprint(apibp)

        from .schemas import ma

        db.init_app(app)
        ma.init_app(app)
        migrate.init_app(app, db)
        # db.create_all()
        admin = setup_admin(app, db)

    @app.route("/functionalmodel/health")
    def health():
        return jsonify("healthy"), 200

    @auth_required
    @app.route("/functionalmodel/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples
        return jsonify(links)

    return app
