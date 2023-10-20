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

        datasets = [a for a in DatasetService().get_all()]

        return [ds["name"] for ds in datasets]


@api_bp.route("/datasets/<string:dataset_name>")
@api_bp.doc("get dataset", security="apikey")
@api_bp.param("dataset_name", "Dataset Name")
class DatasetResource(Resource):
    """Dataset"""

    @auth_required
    @responds(schema=schemas.DatasetSchema)
    def get(self, dataset_name: str) -> schemas.DatasetSchema:
        """Get a Dataset by name"""
        dataset = DatasetService().get_by_name(dataset_name)
        return dataset


@api_bp.route("/datasets/<string:dataset_name>/models")
@api_bp.doc("get models by dataset", security="apikey")
@api_bp.param("dataset_name", "Dataset Name")
class DatasetModelsResource(Resource):
    """Models by Dataset"""

    @auth_required
    @responds(schema=schemas.FunctionalModelSchema(many=True))
    def get(self, dataset_name: str) -> schemas.FunctionalModelSchema:
        """Get a Dataset by name"""
        dataset = DatasetService().get_by_name(dataset_name)
        return FunctionalModelService().get_models_by_dataset_id(dataset.id)


@api_bp.route("/models/<string:model_name>/")
@api_bp.doc("get model by name", security="apikey")
@api_bp.param("model_name", "Model Name")
class ModelResource(Resource):
    """Model"""

    @auth_required
    @responds(schema=schemas.FunctionalModelSchema)
    def get(self, model_name: str) -> schemas.FunctionalModelSchema:
        """Get a Model by name"""
        return FunctionalModelService().get_by_name(model_name)

