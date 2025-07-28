from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobPosting(Base):
    __tablename__ = 'job_postings'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    location = Column(Text)
    description = Column(Text)
    summary = Column(Text)
    level = Column(String)
    department = Column(String)
    skills = Column(String)
    work_model = Column(String)
    posted_at = Column(DateTime)
