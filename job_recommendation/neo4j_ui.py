from database import init_db
from neo4j_db import fetch_jobs_by_skills
from recommender import recommend_jobs
from database import SessionLocal
from models import JobPosting
import streamlit as st

# run streamlit run neo4j_ui.py

session = SessionLocal()

st.set_page_config(page_title="Job Recommender", layout="wide")

st.title("🔍 Smart Job Recommendation Assistant")

# --- Sidebar: User input ---
st.sidebar.header("Your Profile")

skill_input = st.sidebar.text_input(
    "Enter your skills (comma-separated)",
    value="SQL",
    key="skill_input"
)

submit = st.sidebar.button("Find Matching Jobs")


# --- Main Content ---
if submit:
    user_skills = [s.strip() for s in skill_input.split(",") if s.strip()]
    st.success(f"Searching for jobs matching skills: {', '.join(user_skills)}")

    # Step 1: Neo4j filter (optional)
    st.write("🔗 Querying graph for skill-matched jobs...")
    neo4j_job_ids = fetch_jobs_by_skills(user_skills)
    if not matched_jobs:
        st.warning("No matching jobs found in graph.")
    else:
        st.write(f"Found {len(matched_jobs)} skill-matching jobs.")

        # Step 2: Semantic search
        query_text = f"I have skills in {', '.join(user_skills)}. What jobs suit me?"
        st.write("🧠 Running semantic job ranking...")
        results = recommend_jobs(query_text)
        st.write(f"Found {len(results)} llm-matching jobs.")
        filtered_results = [r for r in results if int(r.metadata["id"]) in neo4j_job_ids]
        job_ids = [int(r.metadata["id"]) for r in filtered_results]
        results = filtered_results

        # Step 3: Fetch job details from database
        jobs = session.query(JobPosting).filter(JobPosting.id.in_(job_ids)).all()
        job_dict = {j.id: j for j in jobs}

        # Step 4: Display results
        st.subheader("✅ Top Job Recommendations")
        for result in results:
            job_id = int(result.metadata["id"])
            job = job_dict.get(job_id)
            if not job:
                continue

            with st.expander(f"📌 {job.title}"):
                st.markdown(f"**Location**: {job.location or 'Not specified'}")
                st.markdown(f"**Level**: {job.level or 'Not specified'}")
                st.markdown(f"**Required Skills**: {job.skills or 'N/A'}")

                st.markdown(f"**Why This Job?**\n\n{result.page_content}")

