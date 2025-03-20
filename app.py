from flask import Flask, render_template, request, jsonify
from models.video import db, VideoSummary
from services.youtube import extract_video_id, get_video_info, get_transcript
from services.openai_service import get_summary, analyze_content_quality, answer_question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    # Get all stored summaries
    stored_summaries = VideoSummary.query.order_by(VideoSummary.created_at.desc()).all()
    
    if request.method == "POST":
        video_url = request.form["video_url"]
        try:
            # Extract video ID and check cache
            video_id = extract_video_id(video_url)
            existing_summary = VideoSummary.query.filter_by(video_id=video_id).first()
            if existing_summary:
                return jsonify({
                    'title': existing_summary.title,
                    'summary': existing_summary.summary,
                    'analysis': existing_summary.analysis,
                    'duration_minutes': round(existing_summary.duration / 60),
                    'video_id': existing_summary.video_id,
                    'created_at': existing_summary.created_at.strftime('%Y-%m-%d %H:%M')
                })

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
                transcript=transcript_text,  # Store the transcript
                duration=video_info['duration']
            )
            db.session.add(new_summary)
            db.session.commit()

            return jsonify({
                'title': video_info['title'],
                'summary': summary,
                'analysis': analysis,
                'duration_minutes': round(video_info['duration'] / 60),
                'video_id': video_id,
                'created_at': new_summary.created_at.strftime('%Y-%m-%d %H:%M')
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template("index.html", stored_summaries=stored_summaries)

@app.route("/summary/<video_id>")
def get_summary_by_id(video_id):
    summary = VideoSummary.query.filter_by(video_id=video_id).first()
    if summary:
        return jsonify({
            'title': summary.title,
            'summary': summary.summary,
            'analysis': summary.analysis,
            'duration_minutes': round(summary.duration / 60)
        })
    return jsonify({'error': 'Summary not found'}), 404

@app.route("/summary/<video_id>/ask", methods=["POST"])
def ask_question(video_id):
    try:
        question = request.json.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        summary = VideoSummary.query.filter_by(video_id=video_id).first()
        if not summary:
            return jsonify({'error': 'Summary not found'}), 404

        # Get answer using the transcript
        answer = answer_question(question, summary.transcript)
        return jsonify({'answer': answer.replace('\n', '<br>')})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/summary/<video_id>", methods=["DELETE"])
def delete_summary(video_id):
    try:
        summary = VideoSummary.query.filter_by(video_id=video_id).first()
        if summary:
            db.session.delete(summary)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'error': 'Summary not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)