pip3 install virtualenv

in the folder
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

CREATE A DATABASE IN MAYSQL NAMED prueba


alembic init alembic
####change this line for you DATABASE configuration in alembic.ini

sqlalchemy.url = mysql+pymysql://root:celemin00@localhost:3306/prueba


#in mysql_databse do the same 
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:celemin00@localhost/prueba"

#migrations
alembic upgrade head


#run server
uvicorn main:app --reload



