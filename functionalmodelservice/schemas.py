import functionalmodelservice.models as models
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class DatasetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Dataset


class FunctionalModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.FunctionalModel


class StimulusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Stimulus


class ResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Response
