# import google.generativeai as genai
# from dotenv import load_dotenv
# import os, json
# from services.response_model import BlogPost

# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def generate(prompt, system_msg, model="gemini-1.5-flash") -> BlogPost:
#     m = genai.GenerativeModel(model, system_instruction=system_msg)
#     resp = m.generate_content(prompt)
#     raw = resp.text.strip()
#     if raw.startswith("```"):
#         raw = raw.strip("`").replace("json", "", 1).strip()
#     data = json.loads(raw, strict=False)
#     return BlogPost(**data)




from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from services.response_model import parse_blog_response, BlogPost

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate(prompt, system_msg, model="gemini-3.6-flash") -> BlogPost:
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_msg,
        ),
    )
    raw = resp.text.strip()
    return parse_blog_response(raw)