from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Any

class Parameter(BaseModel):
    id: int
    name: str
    value: Optional[str]

class ParameterName(str, Enum):
    number = "number"
    json = "json"
    boolean = "boolean"
    string = "string"
    array = "array"

class Variable(BaseModel):
    type: str
    value: Any

class ParameterBase(BaseModel):
    name: str
    value: Optional[List[Variable]]

    class Config:
        orm_mode = True
