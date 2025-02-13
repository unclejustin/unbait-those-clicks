import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import openai

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"Error: {e}"

def get_youtube_title(video_url):
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        return f"Error: {e}"

def summarize_text(title, transcript, max_tokens=150):
    prompt = (
        f"Here is a clickbait YouTube video title and its transcript. "
        f"Answer the clickbait title by summarizing the transcript:\n\n"
        f"Title: {title}\n\n"
        f"Transcript: {transcript}\n\n"
        f"Summary:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']

def main():
    video_url = input("Enter YouTube URL: ")
    video_id = video_url.split("v=")[1]  # Extract video ID from URL
    title = get_youtube_title(video_url)
    transcript = get_youtube_transcript(video_id)

    if not transcript.startswith("Error") and not title.startswith("Error"):
        summary = summarize_text(title, transcript)
        print("\nTitle:", title)
        print("\nSummary:\n", summary)
    else:
        print("Error fetching title or transcript:", title, transcript)

if __name__ == "__main__":
    main()