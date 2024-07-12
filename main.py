from typing import Union
from fastapi import FastAPI, Depends, HTTPException, Query
import json


from typing import List
import time
import models
from schemas import ParameterBase, Parameter
import mysql.connector
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, select, join
from sqlalchemy.exc import NoResultFound
from mysql_database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def trasnform_data(type_data, val):

		if type_data == 'number':
			val = int(val)
		elif type_data == 'json':
			val = json.loads(val)
		elif type_data == 'boolean':
			val = bool(val)
		elif type_data == 'string':
			val = str(val)
		elif type_data == 'array':
			
			val = json.loads(val)
			print(val)
		else:
			val = str(val)
		return val
def deafult_value_db (type_data, val):
	if type_data in ["array", "json"]:
		return json.dumps(val)
	else:
		return str(val)






@app.get("/parameters")
def read_parameters(id: int = Query(None, description="Optional parameter id"), db: Session = Depends(get_db)):
	    # Aliases for the tables
        # p = aliased(models.Parameter)
        # tp = aliased(models.TypeParameter)
        # tpm = aliased(models.TypesPerModel)

        # Construct the query
        query = (
            db.query(models.Parameter.name, models.TypeParameter.name, models.TypesPerModel.Value)
            .join(models.TypesPerModel, models.Parameter.id == models.TypesPerModel.parameter_id)
            .join(models.TypeParameter, models.TypeParameter.id == models.TypesPerModel.type_parameter_id)
		)
        if id :
           query.filter(models.Parameter.id == id).one()
        else:
           query.all()

        formatted_results = [
            {"parameter_name": row[0], "type_parameter_name": row[1], "value": trasnform_data(row[1], row[2])}
            for row in query
        ]

        return formatted_results



@app.post("/parameters")
def add_parameter(parameter_:ParameterBase, db: Session = Depends(get_db)) ->None:
	#db_item = models.Parameter(**parameter_.model_dump())
	data = parameter_.model_dump()
	print(data)

	try:
		find_param_db = db.query(models.Parameter).filter(models.Parameter.name == data['name']).one()
	except NoResultFound:
		find_param_db = models.Parameter(name = data['name'])
		db.add(find_param_db)
		db.commit()
		db.flush()
		db.refresh(find_param_db)
            
	types_params = db.query(models.TypeParameter)

	types_params_all = types_params.all() 
	types_names = [type_param.name for type_param in types_params_all]
      
	for value in data['value']:
		if value['type'] in types_names:
			type_param = types_params.filter(models.TypeParameter.name == value['type']).one()
			try:
				conditions = and_(
					models.TypesPerModel.parameter_id == find_param_db.id,
					models.TypesPerModel.type_parameter_id == type_param.id
				)
				type_per_value_param = db.query(models.TypesPerModel).filter(conditions).one()
				type_per_value_param.Value = deafult_value_db (type_param.name, value['value'])
			except NoResultFound:
				type_per_value_param = models.TypesPerModel(parameter_id = find_param_db.id,
										 type_parameter_id = type_param.id,
										 Value = deafult_value_db (type_param.name, value['value']))
				
			finally:
				db.add(type_per_value_param)
				db.commit()
				db.flush()
				db.refresh(type_per_value_param)
	#return data
