from flask import Blueprint, request, jsonify, render_template,redirect, url_for
from models import db, Post

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/save_post", methods=["POST"])
def save_post():
    data = request.get_json()

    post = Post(
        title=data.get("title"),
        meta_description=data.get("meta_description"),
        tags=",".join(data.get("tags", [])),
        body_markdown=data.get("body_markdown"),
        provider=data.get("provider")
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"success": True, "id": post.id})


@posts_bp.route("/dashboard")
def dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("dashboard.html", posts=posts)


@posts_bp.route("/posts/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_view.html", post=post)


@posts_bp.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts.dashboard"))

