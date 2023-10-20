from typing import Type, TypeVar, List, Union
from functionalmodelservice.models import (
    Dataset,
    FunctionalModel,
    Stimulus,
    Response,
)
import cloudfiles
import io
import os
import pandas as pd


T = TypeVar("T")


def fix_local_cloudpath(cloudpath):
    if "://" not in cloudpath:
        dir, _ = os.path.split(cloudpath)
        if len(dir) == 0:
            cloudpath = "./" + cloudpath
        cloudpath = "file://" + cloudpath
    return cloudpath


def read_bytes(path):
    path = fix_local_cloudpath(path)
    cloudpath, file = os.path.split(path)
    cf = cloudfiles.CloudFiles(cloudpath)
    byt = io.BytesIO(cf.get(file))
    return byt


def read_csv(path, **kwargs):
    print("path", path)
    byt = read_bytes(path)
    df = pd.read_csv(byt, **kwargs)
    return df


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

    def get_units_dataframe(self, dataset_name: str):
        dataset = self.get_by_name(dataset_name)
        print(dataset.units_cloudpath)
        # if units_cloudpath is a csv file
        if dataset.units_cloudpath.endswith(".csv"):
            df = read_csv(dataset.units_cloudpath)
            return df
        else:
            raise ValueError("Unknown file type for units_cloudpath")


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

    def get_dataframe(self, stimulus_id: int):
        stim = self.get_by_id(stimulus_id)
        return stim.stimulus_cloudpath


# Extending ModelService for Dataset model
class ResponseService(ModelService):
    def __init__(self):
        super().__init__(Response)

    @staticmethod
    def get_response_by_model(model_id: int) -> List[Response]:
        """returns responses by model

        Args:
            model_id (int): id of model

        Returns:
            List[Response]: Responses that meet this criteria
        """
        return Response.query.filter_by(model_id=model_id).all()

    def get_response_by_stimulus(self, stimulus_id: int) -> List[Response]:
        return Response.query.filter_by(stimulus_id=stimulus_id).all()
