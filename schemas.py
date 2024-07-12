# schemas.py

from pydantic import BaseModel
from enum import Enum, IntEnum
from typing import Union, Optional, Dict, Any, List
from typing_extensions import Literal

class Parameter(BaseModel):
    id : int
    name: str
    value: Optional[str] 

class ParameterName(str, Enum):
    number = "number" 
    json = "json"
    boolean = "boolean"  
    string = "string"
    array = "array"
    

class variable(BaseModel):
    type: str
    value: Any 

class ParameterBase(BaseModel):
    name: str
    value: Optional[List[variable]] 

