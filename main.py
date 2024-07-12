from typing import Union
from fastapi import FastAPI, Depends
import json
# from schemas import cufeIds, Cufe, CufeBase, Event, PersonBase, Person

from typing import List
import time
import models
from schemas import ParameterBase, Parameter
import mysql.connector
from sqlalchemy.orm import Session
from mysql_database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/parameters")
def read_root(parameter_:ParameterBase, db: Session = Depends(get_db)) ->dict:
	db_item = models.Parameter(**parameter_.model_dump())
	data = parameter_.model_dump()
	
	formated_data = []
	for value in data['value']:
		obj = None
		if value is None:
			obj = {"type": "Nulo", "value": value}
		elif isinstance(value, int):
			obj = {"type": "number", "value": value}
		elif isinstance(value, float):
			obj = {"type": "float", "value": value}
		elif isinstance(value, bool):
			obj = {"type": "boolean", "value": value}
		elif isinstance(value, str):
			obj = {"type": "string", "value": value}
		elif isinstance(value, list):
			obj = {"type": "array", "value": value}
		elif isinstance(value, dict):
			obj = {"type": "json", "value": value}
		else:
			raise ValueError("Unsupported type for value")
		formated_data.append(obj)
		
	
	data["value"] = str(formated_data)

	db_item = models.Parameter(**data)
	db.add(db_item)
	db.commit()
	db.flush()
	db.refresh(db_item)

	return data
