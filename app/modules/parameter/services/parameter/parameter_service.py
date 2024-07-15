import json
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from app.modules.parameter.entities import models
from app.modules.parameter.entities.schemas import ParameterBase
from app.modules.parameter.services.parameter.parameter_interface import ParameterInterface

class ParameterService(ParameterInterface):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def _transform_type_parameter_value(self, type_data: str, val: str) ->  Union[str, dict]:
        if type_data in ["array", "json"]:
            return json.dumps(val)
        else:
            return str(val)

    def _get_type_parameter_value(self, type_data: str, val: str) -> str:
        if type_data in ['number', 'boolean']:
            return int(val) if type_data == 'number' else bool(val)
        elif type_data in ['json', 'array']:
            return json.loads(val)
        else:
            return str(val)

    def create_parameter(self, parameter_: ParameterBase) -> int:
        data = parameter_.model_dump()
        
        try:
            find_param_db = self.db.query(models.Parameter).filter(models.Parameter.name == data['name']).one()
        except NoResultFound:
            find_param_db = models.Parameter(name=data['name'])
            self.db.add(find_param_db)
            self.db.commit()
            self.db.refresh(find_param_db)

        types_params = self.db.query(models.TypeParameter).all()
        types_names = {type_param.name for type_param in types_params}

        for value in data['value']:
            if value['type'] in types_names:
                type_param = next(tp for tp in types_params if tp.name == value['type'])
                try:
                    type_per_value_param = (
                        self.db.query(models.TypesPerModel)
                        .filter(and_(
                            models.TypesPerModel.parameter_id == find_param_db.id,
                            models.TypesPerModel.type_parameter_id == type_param.id
                        ))
                        .one()
                    )
                    type_per_value_param.Value = self._transform_type_parameter_value(type_param.name, value['value'])
                except NoResultFound:
                    type_per_value_param = models.TypesPerModel(
                        parameter_id=find_param_db.id,
                        type_parameter_id=type_param.id,
                        Value=self._transform_type_parameter_value(type_param.name, value['value'])
                    )
                    self.db.add(type_per_value_param)

        self.db.commit()
        return find_param_db.id

    def get_parameter(self, id: int = None) -> List[dict]:
        query = (
            self.db.query(models.Parameter.name, models.TypeParameter.name, models.TypesPerModel.Value)
            .join(models.TypesPerModel, models.Parameter.id == models.TypesPerModel.parameter_id)
            .join(models.TypeParameter, models.TypeParameter.id == models.TypesPerModel.type_parameter_id)
        )
        if id is not None:
            query = query.filter(models.Parameter.id == id).one()
        else:
            query = query.all()

        formatted_results = [
            {"parameter_name": row[0], "type_parameter_name": row[1], "value": self._get_type_parameter_value(row[1], row[2])}
            for row in query
        ]

        return formatted_results
