# seed_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.modules.parameter.entities.models import TypeParameter
from sqlalchemy.orm import Session
from repositories.db.mysql_database import SessionLocal


# Replace 'your_sqlalchemy_module' with the module where your SQLAlchemy Base and TypeParameter class are defined.

# Define your initial data
initial_data = [
    {"name": "number"},
    {"name": "json"},
    {"name": "boolean"},
    {"name": "string"},
    {"name": "array"},
    
    # Add more entries as needed
]




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    db: Session = SessionLocal()
    # Seed data into the TypeParameter table
    for entry in initial_data:
        parameter = TypeParameter(**entry)
        db.add(parameter)
    
    # Commit the changes
    db.commit()
    print("Seed data inserted successfully.")

except IntegrityError as e:
    db.rollback()
    print(f"Error inserting seed data: {e}")

finally:
    # Close the session
    db.close()
