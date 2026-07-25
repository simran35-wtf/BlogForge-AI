from flask import Blueprint, request, jsonify
from services.model_provider import generate_content, generate_compare
from services.prompts import build_blog_prompt, BLOG_SYSTEM_PROMPT

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate_blog", methods=["POST"])
def generate_blog():
    data = request.get_json()
    provider = data.get("provider", "groq")
    topic = data.get("topic")

    if not topic:
        return jsonify({"success": False, "error": "Topic is required"}), 400

    try:
        post = generate_content(
            provider=provider,
            prompt=build_blog_prompt(topic),
            system_msg=BLOG_SYSTEM_PROMPT
        )
        return jsonify({
            "success": True,
            "provider": provider,
            "title": post.title,
            "meta_description": post.meta_description,
            "tags": post.tags,
            "body_markdown": post.body_markdown
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@generate_bp.route("/compare_blog", methods=["POST"])
def compare_blog():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"success": False, "error": "Topic is required"}), 400

    try:
        results = generate_compare(
            prompt=build_blog_prompt(topic),
            system_msg=BLOG_SYSTEM_PROMPT
        )
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500