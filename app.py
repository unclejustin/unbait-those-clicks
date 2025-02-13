from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from openai import OpenAI
from urllib.parse import urlparse, parse_qs
import time

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def extract_video_id(url):
    """Extract video ID from various forms of YouTube URLs."""
    # Handle different URL formats (including shortened ones)
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        elif parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    # If no match found
    raise ValueError('Invalid YouTube URL')

def get_video_info(url):
    """Get video information using yt-dlp."""
    try:
        print(f"Trying URL: {url}")
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Created YoutubeDL object")
            info = ydl.extract_info(url, download=False)
            print("Successfully extracted info")
            return {
                'title': info.get('title'),
                'duration': info.get('duration', 0)  # Duration in seconds
            }
            
    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise Exception("Could not access video. Please verify the URL is correct and the video is public.")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        try:
            # Extract video ID using the new function
            video_id = extract_video_id(video_url)

            # Fetch video info using yt-dlp
            video_info = get_video_info(video_url)
            title = video_info['title']
            duration_minutes = round(video_info['duration'] / 60)  # Convert seconds to minutes

            # Fetch transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript])

            # Summarize using OpenAI
            prompt = (
                f"Here is a clickbait YouTube video title and its transcript. "
                f"Please provide a concise summary of the main points. "
                f"If the title mentions a specific number (like '7 things' or '5 tips'), "
                f"extract exactly that number of key points from the video and format them as a numbered list. "
                f"Otherwise, provide a paragraph summary. "
                f"Make sure to capture all the points mentioned in the video if it's a list-style video.\n\n"
                f"Title: {title}\n\n"
                f"Transcript: {transcript_text}\n\n"
                f"Summary:"
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, complete summaries. For numbered lists in videos, you ensure you capture all points mentioned."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            summary = response.choices[0].message.content
            # Replace newlines with <br> tags
            summary = summary.replace('\n', '<br>')

            return render_template(
                "index.html", 
                title=title, 
                summary=summary, 
                duration_minutes=duration_minutes
            )

        except Exception as e:
            error_message = f"Error processing video: {str(e)}"
            return render_template("index.html", error=error_message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)