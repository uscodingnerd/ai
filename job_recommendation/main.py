from datetime import datetime
from crawler import crawl_jobs
from llm_classifier import classify_job
from models import JobPosting
from database import init_db, SessionLocal, print_all
from recommender import build_vector_index

init_db()
jobs = crawl_jobs()
session = SessionLocal()
print(len(jobs))
job_no = 0
for job in jobs:
    enriched = classify_job(job)
    print(enriched)
    clean_str = job['posted_at'].replace("Posted ", "")
    dt = datetime.strptime(clean_str, "%B %d, %Y")
    skills_str = ",".join(enriched['skills'])
    job_entry = JobPosting(
        title=job['title'],
        location=job['location'],
        description=job['description'],
        summary=enriched['summary'],
        level=enriched['level'],
        department=enriched['department'],
        skills=",".join(enriched['skills']),
        work_model=enriched['work_model'],
        posted_at=dt
    )
    session.add(job_entry)
    job_no += 1
    # if job_no > 3:
    #     break

session.commit()
# print_all()

build_vector_index()

