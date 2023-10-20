from typing import List
from functionalmodelservice.models import (
    Dataset,
    FunctionalModel,
    Stimulus,
    Response,
)

from typing import Type, TypeVar, List, Union

T = TypeVar("T")


class ModelService:
    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self) -> List[T]:
        return self.model.query.all()

    def get_by_name(self, name: str) -> Union[T, None]:
        return self.model.query.filter_by(name=name).first()

    def get_by_id(self, id_: int) -> Union[T, None]:
        return self.model.query.filter_by(id=id_).first()


# Extending ModelService for Dataset model
class DatasetService(ModelService):
    def __init__(self):
        super().__init__(Dataset)


class FunctionalModelService(ModelService):
    def __init__(self):
        super().__init__(FunctionalModel)

    def get_models_by_dataset_id(self, dataset_id: int) -> List[FunctionalModel]:
        """gets a model by dataset id

        Args:
            dataset_id (int): dataset id

        Returns:
            List[FunctionalModel]: list of models trained on this dataset
        """
        return FunctionalModel.query.filter_by(dataset_id=dataset_id).all()


# Extending ModelService for Dataset model
class StimulusService(ModelService):
    def __init__(self):
        super().__init__(Stimulus)


# Extending ModelService for Dataset model
class ResponseService(ModelService):
    def __init__(self):
        super().__init__(Response)

    def get_response_by_model(self, model_id: int) -> List[Response]:
        """returns responses by model

        Args:
            model_id (int): id of model

        Returns:
            List[Response]: Responses that meet this criteria
        """
        return Response.query.filter_by(model_id=model_id).all()
    
    def get_response_by_stimulus(self, stimulus_id: int) -> List[Response]:
        return Response.query.filter_by(stimulus_id=stimulus_id).all()
    