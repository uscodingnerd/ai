from openai import OpenAI
import json

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)


def gen_cypher(job):
    prompt = f"""
You are a Neo4j Cypher expert. Given the following job title and description, extract:
Title: {job.title}
Description: {job.description}

Creates a Job node with title and id
Links to a Company node
Adds required Skill nodes
Optionally links Location, Industry, and Level

Extract:
- Job title
- Department
- Skills
- Location
- Industry
- Experience (optional)

Then generate Cypher code to insert this job posting into a Neo4j graph.
Only output pure Cypher code. No markdown or explanation.
If info is null, use ""Not Specified""
Remove the triple quote in the final result
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    return content
