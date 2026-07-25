# services/prompts.py

# BLOG_SYSTEM_PROMPT = "You are an expert blog writer and SEO strategist."

# def build_blog_prompt(topic: str, tone: str = "engaging", word_count: int = 900) -> str:
#     return f"""
# Write a blog post about: {topic}

# Tone: {tone}
# Target length: ~{word_count} words

# Structure the post exactly like this:
# - A viral-worthy, SEO-friendly headline
# - ## Introduction — an engaging hook and context
# - ## 3 body sections with clear subheadings — include examples, stats, or practical insights
# - ## Key Takeaways — 3 bullet points, shareable and concise
# - ## Sources — if you reference any facts, note them here (can be general, no live links needed)

# Return ONLY valid JSON matching this exact schema, no extra text:
# {{
#   "title": "...",
#   "meta_description": "under 160 characters",
#   "tags": ["tag1", "tag2", "tag3"],
#   "body_markdown": "the full post in markdown, starting from ## Introduction"
# }}
# """


BLOG_SYSTEM_PROMPT = "You are an expert blog writer and SEO strategist."

def build_blog_prompt(topic: str, tone: str = "engaging", word_count: int = 900) -> str:
    return f"""
Write a blog post about: {topic}

Tone: {tone}
Target length: ~{word_count} words

Return your response in EXACTLY this format, using these exact markers. Do not use JSON. Do not add any text before TITLE: or after the end of SOURCES.

TITLE: <the blog title here, one line>
META: <meta description, under 160 characters, one line>
TAGS: <tag1, tag2, tag3>
BODY_START
<full blog post in markdown here — intro, 3 sections with headings, key takeaways, sources — can span multiple lines>
BODY_END
"""