# Import flask dependencies
from flask import jsonify, render_template, current_app, make_response, Blueprint
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from middle_auth_client import (
    auth_required,
    auth_requires_permission,
    user_has_permission,
)
from functionalmodelservice.data_serialization import create_df_response
from functionalmodelservice import schemas
from functionalmodelservice.service import (
    DatasetService,
    FunctionalModelService,
    StimulusService,
    ResponseService,
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


@api_bp.route("/datasets/<string:dataset_name>/units")
@api_bp.doc("get units by dataset", security="apikey")
@api_bp.param("dataset_name", "Dataset Name")
class DatasetUnitsResource(Resource):
    """Units by Dataset"""

    @auth_required
    def get(self, dataset_name: str):
        """Get a Dataset by name"""
        dss = DatasetService()
        df = dss.get_units_dataframe(dataset_name)
        print(df)
        return create_df_response(df, [])


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


@api_bp.route("/models/<string:model_name>/responses")
@api_bp.doc("get responses by model", security="apikey")
@api_bp.param("model_name", "Model Name")
class ModelResponsesResource(Resource):
    """Responses by Model"""

    @auth_required
    @responds(schema=schemas.ResponseSchema(many=True))
    def get(self, model_name: str) -> schemas.ResponseSchema:
        """Get a Model by name"""
        model = FunctionalModelService().get_by_name(model_name)
        return ResponseService().get_response_by_model(model.id)


@api_bp.route("/responses/<int:response_id>")
@api_bp.doc("get response by id", security="apikey")
@api_bp.param("response_id", "Response ID")
class ResponseResource(Resource):
    """Response"""

    @auth_required
    @responds(schema=schemas.ResponseSchema)
    def get(self, response_id: int) -> schemas.ResponseSchema:
        """Get a Response by id"""
        return ResponseService().get_by_id(response_id)


@api_bp.route("/responses/<int:response_id>/stimulus")
@api_bp.doc("get stimulus by response id", security="apikey")
@api_bp.param("response_id", "Response ID")
class ResponseStimulusResource(Resource):
    """Response"""

    @auth_required
    @responds(schema=schemas.StimulusSchema)
    def get(self, response_id: int) -> schemas.StimulusSchema:
        """Get a Response by id"""
        response = ResponseService().get_by_id(response_id)
        return StimulusService().get_by_id(response.stimulus_id)


@api_bp.route("/responses/<int:response_id>/stimulus/metadata")
@api_bp.doc("get stimulus data by response id", security="apikey")
@api_bp.param("response_id", "Response ID")
class ResponseStimulusDataResource(Resource):
    """Response"""

    @auth_required
    @responds(schema=schemas.StimulusSchema)
    def get(self, response_id: int):
        """Get a Response by id"""
        response = ResponseService().get_by_id(response_id)
        return jsonify(StimulusService().get_dataframe(response.stimulus_id))
