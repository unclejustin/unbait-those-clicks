# Unbait those clicks! 🎣

A web app that saves you time by summarizing clickbait YouTube videos. Simply paste a YouTube URL, and get a concise summary of the video's content. No more sitting through long-winded videos to get to the point!

## Features

- 🎯 Extracts key points from YouTube videos
- 📝 Provides concise, readable summaries
- 🔢 Automatically formats numbered lists (e.g., "5 tips", "10 things")
- ⏱️ Shows how many minutes you saved
- 💨 Supports various YouTube URL formats

## Setup

1. Clone the repository

2. (Recommended) Create a virtual environment:

   > A virtual environment keeps the project's packages separate from your system Python installation

   ```bash
   # Create the virtual environment
   python -m venv venv

   # Activate it on Mac/Linux:
   source venv/bin/activate

   # Or on Windows:
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the App

1. If using a virtual environment, make sure it's activated (you'll see `(venv)` in your terminal)

2. Start the Flask server:

   ```bash
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies (installed via requirements.txt):
  - Flask
  - python-dotenv
  - openai
  - yt-dlp
  - youtube-transcript-api

## How It Works

1. Uses yt-dlp to fetch video information
2. Gets the video transcript using youtube-transcript-api
3. Processes the transcript using OpenAI's GPT-4 to create a concise summary
4. Formats the summary based on video content (numbered lists for list-style videos, paragraphs for regular content)

## Limitations

- Only works with YouTube videos that have transcripts available
- Requires an OpenAI API key
- Video must be publicly accessible
