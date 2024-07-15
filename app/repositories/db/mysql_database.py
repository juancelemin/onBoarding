from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Mysql_connector:
    def __init__(self) -> None:
        # MySQL connection URL
        SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost/prueba"
        # Create MySQL database engine
        _engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=10,  # Adjust pool_size as needed
            pool_recycle=1800,  # Adjust pool_recycle as needed
        )
        # Create session maker
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

        
        # Create SQLAlchemy Base
        Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
