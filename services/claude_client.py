# services/claude_client.py
import anthropic, os, json
from services.response_model import BlogPost

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate(prompt, system_msg, model="claude-sonnet-4-6") -> BlogPost:
    resp = client.messages.create(
        model=model,
        max_tokens=1500,
        system=system_msg,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.content[0].text
    data = json.loads(raw)
    return BlogPost(**data)