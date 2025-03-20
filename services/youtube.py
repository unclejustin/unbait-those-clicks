from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract video ID from various forms of YouTube URLs."""
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
    raise ValueError('Invalid YouTube URL')

def get_video_info(url):
    """Get video information using yt-dlp."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'duration': info.get('duration', 0)
            }
            
    except Exception as e:
        raise Exception("Could not access video. Please verify the URL is correct and the video is public.")

def get_transcript(video_id):
    """Get video transcript."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry['text'] for entry in transcript]) 