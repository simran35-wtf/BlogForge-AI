from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    meta_description = db.Column(db.String(300))
    tags = db.Column(db.String(300))  # comma-separated string
    body_markdown = db.Column(db.Text, nullable=False)
    provider = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "meta_description": self.meta_description,
            "tags": self.tags.split(",") if self.tags else [],
            "body_markdown": self.body_markdown,
            "provider": self.provider,
            "created_at": self.created_at.strftime("%d %b %Y, %I:%M %p")
        }