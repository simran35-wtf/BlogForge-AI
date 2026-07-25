# services/response_model.py
# from pydantic import BaseModel
# from typing import List


# class BlogPost(BaseModel):
#     title: str
#     meta_description: str
#     tags: List[str]
#     body_markdown: 



import re
from pydantic import BaseModel
from typing import List


class BlogPost(BaseModel):
    title: str
    meta_description: str
    tags: List[str]
    body_markdown: str


def parse_blog_response(raw: str) -> BlogPost:
    title_match = re.search(r"TITLE:\s*(.+)", raw)
    meta_match = re.search(r"META:\s*(.+)", raw)
    tags_match = re.search(r"TAGS:\s*(.+)", raw)
    body_match = re.search(r"BODY_START\s*(.*?)\s*BODY_END", raw, re.DOTALL)

    title = title_match.group(1).strip() if title_match else "Untitled"
    meta = meta_match.group(1).strip() if meta_match else ""
    tags_raw = tags_match.group(1).strip() if tags_match else ""
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    body = body_match.group(1).strip() if body_match else raw

    return BlogPost(title=title, meta_description=meta, tags=tags, body_markdown=body)