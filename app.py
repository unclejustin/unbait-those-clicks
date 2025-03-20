from flask import Flask, render_template, request
from models.video import db, VideoSummary
from services.youtube import extract_video_id, get_video_info, get_transcript
from services.openai_service import get_summary, analyze_content_quality

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        try:
            # Extract video ID and check cache
            video_id = extract_video_id(video_url)
            existing_summary = VideoSummary.query.filter_by(video_id=video_id).first()
            if existing_summary:
                return render_template(
                    "index.html",
                    title=existing_summary.title,
                    summary=existing_summary.summary,
                    analysis=existing_summary.analysis,
                    duration_minutes=round(existing_summary.duration / 60)
                )

            # Get video info and transcript
            video_info = get_video_info(video_url)
            transcript_text = get_transcript(video_id)
            
            # Get summary and analysis
            summary = get_summary(video_info['title'], transcript_text)
            analysis = analyze_content_quality(video_info['title'], transcript_text, summary)

            # Format for display
            summary = summary.replace('\n', '<br>')
            analysis = analysis.replace('\n', '<br>')

            # Store in database
            new_summary = VideoSummary(
                video_id=video_id,
                title=video_info['title'],
                summary=summary,
                analysis=analysis,
                duration=video_info['duration']
            )
            db.session.add(new_summary)
            db.session.commit()

            return render_template(
                "index.html",
                title=video_info['title'],
                summary=summary,
                analysis=analysis,
                duration_minutes=round(video_info['duration'] / 60)
            )

        except Exception as e:
            error_message = f"Error processing video: {str(e)}"
            return render_template("index.html", error=error_message)

    return render_template("index.html")

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)