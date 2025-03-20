from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VideoSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    transcript = db.Column(db.Text, nullable=False)  # Store the full transcript
    duration = db.Column(db.Integer, nullable=False)  # in seconds
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Video {self.title}>' 