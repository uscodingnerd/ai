from database import init_db, SessionLocal, get_all
from neo4j_llm_cypher_gen import gen_cypher
from neo4j_db import run_script

init_db()
session = SessionLocal()
jobs = get_all()
i = 0
for job in jobs:
    try:
        script = gen_cypher(job)
        print(script)
        # run_script(script)
    except Exception as e:
        print(f"Failed to run script: {e}")

    i += 1