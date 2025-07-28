import streamlit as st
from recommender import recommend_jobs
from database import SessionLocal
from models import JobPosting

# run streamlit run streamlit_app.py
# Setup
st.set_page_config(page_title="Job Recommender", layout="wide")

st.title("🔍 Referral Job Recommendation System")

# Input box
# What jobs fit someone with ML + cloud skills
# I am good at english and Japanese
query = st.text_input("Enter your interests, skills, or desired job (e.g., 'Python backend remote'):")

# Filters
col1, col2 = st.columns(2)
with col1:
    selected_level = st.selectbox("Job Level", ["Any", "Entry", "Mid", "Senior"])
with col2:
    selected_model = st.selectbox("Search Method", ["Semantic (AI)", "Keyword"])

# Recommend
if query:
    st.info("Searching for jobs...")
    session = SessionLocal()

    if selected_model == "Semantic (AI)":
        results = recommend_jobs(query)
        job_ids = [int(r.metadata["id"]) for r in results]
        jobs = session.query(JobPosting).filter(JobPosting.id.in_(job_ids)).all()
    else:
        # Keyword search fallback (basic)
        jobs = session.query(JobPosting).filter(
            JobPosting.description.ilike(f"%{query}%")
        ).all()

    # Optional filter
    if selected_level != "Any":
        jobs = [j for j in jobs if j.level.lower() == selected_level.lower()]

    # Display results
    st.success(f"Found {len(jobs)} job(s):")

    for job in jobs:
        with st.expander(f"💼 {job.title} — {job.location}"):
            st.markdown(f"**Level**: {job.level}")
            st.markdown(f"**Department**: {job.department}")
            st.markdown(f"**Skills**: {job.skills}")
            st.markdown(f"**Work Model**: {job.work_model}")
            st.markdown(f"**Summary**: {job.summary}")

else:
    st.warning("Enter a query to get job recommendations.")