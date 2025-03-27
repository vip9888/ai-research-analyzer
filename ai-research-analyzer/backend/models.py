from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class ResearchPaper(Base):
    __tablename__="research_papers"  #this is sqlalchemy syntax of defining the table name, this ensures which table in the database this model maps to

    id=Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    summary = Column(Text)
    content = Column(Text)
    filepath = Column(String(255))