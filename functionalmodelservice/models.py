from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from functionalmodelservice.database import Base


class NamedModel(object):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return "{}({})".format(self.name, self.id)

    def __getitem__(self, field):
        return self.__dict__[field]


class Dataset(NamedModel, Base):
    project = Column(String(200), nullable=False)
    units_cloudpath = Column(String(200), nullable=False)


class TrainedFunctionalModel(NamedModel, Base):
    __tablename__ = "image_source"
    replaced_by = Column(Integer, ForeignKey("Model.id"), nullable=True)
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    dataset = relationship("Dataset")


class Stimuli(NamedModel, Base):
    __tablename__ = "aligned_volume"
    stimulus_cloudpath = Column(String(200), nullable=False)
    stimulus_metadata_cloudpath = Column(String(200), nullable=False)


class ModeledResponses(Base):
    id = Column(Integer, primary_key=True)
    stimulus_id = Column(Integer, ForeignKey("stimuli.id"))
    stimulus = relationship("Stimuli")
    model_id = Column(Integer, ForeignKey("Model.id"))
    model = relationship("Model")
    responses_cloudpath = Column(String(200), nullable=False)
