from openai import OpenAI
import os, json
from services.response_model import BlogPost

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate(prompt, system_msg, model="gpt-4o-mini") -> BlogPost:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").replace("json", "", 1).strip()
    data = json.loads(raw)
    return BlogPost(**data)