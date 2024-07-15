from typing import Union
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from app.modules.parameter.entities.schemas import ParameterBase, Parameter
from sqlalchemy.orm import Session
from app.repositories.db.mysql_database import Mysql_connector
from app.modules.parameter.services.parameter.parameter_service import ParameterService

app = FastAPI()
mysql_db = Mysql_connector()

@app.get("/parameters")
def read_parameters(id: int = Query(None, description="Optional parameter id"), db: Session = Depends(mysql_db.get_db)):
	
	parameterService = ParameterService( db)
	if not parameterService:
		raise HTTPException(status_code=404, detail="Item not found")

	return parameterService.get_parameter(id)

@app.post("/parameters")
def add_parameter(parameter_:ParameterBase, db: Session = Depends(mysql_db.get_db)) -> int:
	parameterService = ParameterService( db)
	
	return parameterService.create_parameter(parameter_= parameter_)
	
