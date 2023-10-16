import functionalmodelservice.models as models
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class DatasetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Dataset


class TrainedFunctionalModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.TrainedFunctionalModel


class StimuliSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Stimuli


class ModeledResponsesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.ModeledResponses

