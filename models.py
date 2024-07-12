from typing import Union, Dict, Any, List, Optional
from sqlalchemy import Column, Integer, String, Boolean, TypeDecorator, Text

import json

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base





Base = declarative_base()


class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(500), nullable= False)

class TypeParameter(Base):
    __tablename__ = "type_parameters"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(500), nullable= False)

class TypesPerModel(Base):
    __tablename__ = "types_per_model"
    id = Column(Integer, primary_key=True, index=True)
    Value = Column(Text, nullable= False)
    parameter_id = Column(Integer, ForeignKey("parameters.id"))
    type_parameter_id = Column(Integer, ForeignKey("type_parameters.id"))

    parameter = relationship("Parameter", backref="types_per_model")
    type_parameter = relationship("TypeParameter", backref="types_per_model")