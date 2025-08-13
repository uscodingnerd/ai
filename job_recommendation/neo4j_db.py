from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "11111111")) # 11111111


# Define the function to create nodes and relationships
def create_data(tx, script):
    tx.run(script)


# Run the function in a Neo4j session
def run_script(script):
    with driver.session() as session:
        session.execute_write(create_data, script)
        print("Graph created!")
    driver.close()


def fetch_jobs_by_skills(skills):
    with driver.session() as session:
        result = session.run("""
        UNWIND $skills AS skillName
        MATCH (j:Job)-[:REQUIRES]->(s:Skill {name: skillName})
        RETURN DISTINCT j.title AS job_title, j.id AS job_id
        LIMIT 10
        """, skills=skills)

        jobs = [record["job_id"] for record in result]

    driver.close()
    return jobs

