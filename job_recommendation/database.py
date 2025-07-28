from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import JobPosting


engine = create_engine("sqlite:///jobs.db")
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_all():
    session = SessionLocal()
    return session.query(JobPosting)


def print_all():
    session = SessionLocal()
    for job in session.query(JobPosting):
        print(job.skills)