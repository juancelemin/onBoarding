# schemas.py

from pydantic import BaseModel
from typing import Union, Optional, Dict, Any, List

class Parameter(BaseModel):
    id : int
    name: str
    value: Optional[str] 


class ParameterBase(BaseModel):
    name: str
    value: Optional[List[Any]] 

