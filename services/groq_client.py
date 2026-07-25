# from groq import Groq
# from dotenv import load_dotenv
# import os, json
# from services.response_model import BlogPost

# load_dotenv() 

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def generate(prompt, system_msg, model="llama-3.3-70b-versatile") -> BlogPost:
#     resp = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7,
#         max_tokens=1500
#     )
#     raw = resp.choices[0].message.content.strip()
#     if raw.startswith("```"):
#         raw = raw.strip("`").replace("json", "", 1).strip()
#     data = json.loads(raw, strict=False)
#     return BlogPost(**data)


from groq import Groq
from dotenv import load_dotenv
import os
from services.response_model import parse_blog_response, BlogPost

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate(prompt, system_msg, model="llama-3.3-70b-versatile") -> BlogPost:
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
    return parse_blog_response(raw)