# seed_data.py

from sqlalchemy.exc import IntegrityError
from app.modules.parameter.entities.models import TypeParameter
from app.repositories.db.mysql_database import Mysql_connector

class TypeParameterSeed:
    def __init__(self) -> None:
        pass
        initial_data = [
            {"id": 1, "name": "number"},
            {"id": 2, "name": "json"},
            {"id": 3, "name": "boolean"},
            {"id": 4, "name": "string"},
            {"id": 5, "name": "array"},
            
        ]
        mysql_db = Mysql_connector()

        try:
            db = mysql_db.get_db()
            # Seed data into the TypeParameter table
            for entry in initial_data:
                parameter = TypeParameter(**entry)
                db.add(parameter)
            
            # Commit the changes
            db.commit()
            print("Seed data inserted successfully.")

        except IntegrityError as e:
            db.rollback()
            print(f"Error inserting seed data: {"id": e}")

        finally:
            # Close the session
            db.close()