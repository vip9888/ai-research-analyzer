from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/researchdb"

engine = create_engine(DATABASE_URL) # create_engine(DATABASE_URL) initializes the database connection, It allows SQLAlchemy to execute SQL queries on MySQL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # This Base class is used to define all ORM models, Every model (like ResearchPaper) must inherit from Base.

# Dependency function to get DB session
def get_db(): # Ensures a clean session for querying models like ResearchPaper.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()