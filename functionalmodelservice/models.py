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
    __tablename__ = "dataset"
    project = Column(String(200), nullable=False)
    units_cloudpath = Column(String(200), nullable=False)


class FunctionalModel(NamedModel, Base):
    __tablename__ = "functionalmodel"
    replaced_by = Column(Integer, ForeignKey("functionalmodel.id"), nullable=True)
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    dataset = relationship("Dataset")
    description = Column(String(500), nullable=False)


class Stimulus(NamedModel, Base):
    __tablename__ = "stimulus"
    stimulus_cloudpath = Column(String(200), nullable=False)
    stimulus_metadata_cloudpath = Column(String(200), nullable=False)
    length = Column(Integer, nullable=False)


class Response(Base):
    __tablename__ = "response"
    id = Column(Integer, primary_key=True)
    stimulus_id = Column(Integer, ForeignKey("stimulus.id"))
    stimulus = relationship("Stimulus")
    model_id = Column(Integer, ForeignKey("functionalmodel.id"))
    model = relationship("FunctionalModel")
    responses_cloudpath = Column(String(200), nullable=False)
