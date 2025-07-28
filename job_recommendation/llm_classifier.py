from openai import OpenAI
import json

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)


def classify_job(job):
    prompt = f"""
Title: {job['title']}
Description: {job['description']}

Extract:
- level (entry/mid/senior)
- department
- skills
- work_model (Remote/Hybrid/Onsite)
- summary (1-2 sentences)

Only output pure JSON. No markdown or explanation.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)
