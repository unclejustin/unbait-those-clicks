from flask import Blueprint, request, jsonify
from models.video import VideoSummary
from services.openai_service import answer_question
from extensions import db

summary = Blueprint('summary', __name__)

@summary.route("/summary/<video_id>")
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

@summary.route("/summary/<video_id>/ask", methods=["POST"])
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

@summary.route("/summary/<video_id>", methods=["DELETE"])
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