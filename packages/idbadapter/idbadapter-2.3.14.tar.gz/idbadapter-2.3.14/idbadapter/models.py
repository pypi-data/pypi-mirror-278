from abc import abstractmethod

from sqlalchemy import Column, Float, Integer, ForeignKey, String, JSON, Identity
from sqlalchemy.ext.declarative import declarative_base

MSCHM_Base = declarative_base()

class MSCHMModel(MSCHM_Base):

    __abstract__ = True

    @property
    @abstractmethod
    def __tablename__(self) -> str:
        pass

    @classmethod
    def get_key(cls, key: str):
        return f'{cls.__tablename__}.{key}'

    @classmethod
    def get_key_id(cls):
        return cls.get_key("id")

    id = Column(Integer, Identity(start=1), primary_key=True)

class BasicWork(MSCHMModel):

    __tablename__ = "basic_works"

    name = Column(String, nullable=False)


class BasicResource(MSCHMModel):

    __tablename__ = "basic_resources"

    name = Column(String, nullable=False)


class Precalculation(MSCHMModel):

    __tablename__ = "precalculations"

    work_value = Column(Float, nullable=False)
    res_value = Column(Float, nullable=False)
    probability = Column(Integer, nullable=False)
    work_value_probability = Column(Float, nullable=False)

    # Foreign Keys
    id_basic_work = Column(Integer, ForeignKey(BasicWork.get_key_id()), nullable=False, index=True)
    id_basic_resource = Column(Integer, ForeignKey(BasicResource.get_key_id()), nullable=False, index=True)

class MSModel(MSCHMModel):
    __tablename__ = "mschm_model"

    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    measurement_type = Column(String, nullable=True)

class S7Model(MSCHMModel):
    __tablename__ = "s7_mschm_model"

    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

