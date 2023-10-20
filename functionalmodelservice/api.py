# Import flask dependencies
from flask import jsonify, render_template, current_app, make_response, Blueprint
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from functionalmodelservice import schemas
from functionalmodelservice.service import (
    DatasetService,
    FunctionalModelService,
    StimulusService,
    ResponseService,
)
from typing import List
from middle_auth_client import (
    auth_required,
    auth_requires_permission,
    user_has_permission,
)

__version__ = "0.0.1"

authorizations = {
    "apikey": {"type": "apiKey", "in": "query", "name": "middle_auth_token"}
}

api_bp = Namespace(
    "Functional Model Response Service",
    authorizations=authorizations,
    description="service for serving responses to stimuli",
)


@api_bp.route("/datasets")
@api_bp.doc("get datasets", security="apikey")
class DatasetsResource(Resource):
    """Datasets"""

    @auth_required
    def get(self) -> List:
        """Get all Datasets"""
        datasets = [a for a in DatasetService.get_all()]

        return [ds["name"] for ds in datasets]
