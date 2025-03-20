from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_summary(title, transcript_text):
    """Get video summary from OpenAI."""
    summary_prompt = (
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
            {"role": "user", "content": summary_prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content

def analyze_content_quality(title, transcript_text, summary):
    """Analyze video content quality."""
    prompt = (
        f"Analyze this YouTube video's content quality by comparing the full transcript with its summary. "
        f"Start your response with a clear 'Watch: YES' or 'Watch: NO' on the first line.\n\n"
        f"Be very strict with your recommendation - only say YES if the video contains significant value "
        f"that cannot be effectively captured in the summary, such as:\n"
        f"- Critical visual demonstrations or examples\n"
        f"- Complex technical explanations that benefit from visual aids\n"
        f"- Important nuanced discussions that lose meaning without tone and context\n"
        f"- Unique interactive elements or real-time demonstrations\n\n"
        f"Say NO if the video primarily contains:\n"
        f"- Personal anecdotes that don't add substantial value\n"
        f"- Repetitive explanations or filler content\n"
        f"- Information that is equally effective in written form\n"
        f"- Generic advice without specific actionable details\n\n"
        f"Then analyze:\n"
        f"1. Signal-to-noise ratio (be specific about percentage of meaningful content)\n"
        f"2. What specific value, if any, the full video provides beyond the summary\n"
        f"3. Whether any crucial context is lost in the summary\n\n"
        f"After your Yes/No recommendation, provide a brief analysis explaining why, and specify whether someone should:\n"
        f"A) Just read the summary\n"
        f"B) Watch specific parts of the video (if yes, which parts)\n"
        f"C) Watch the entire video\n\n"
        f"Title: {title}\n\n"
        f"Summary: {summary}\n\n"
        f"Full Transcript: {transcript_text}\n\n"
        f"Analysis:"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a strict content analyst who values people's time above all else. "
                          "Always start with a clear Watch: YES or Watch: NO recommendation before providing your analysis. "
                          "Be very conservative with YES recommendations - only recommend watching if the video provides "
                          "substantial value that cannot be effectively conveyed in text form. "
                          "Your goal is to save people from watching videos that don't provide significant value beyond their summary."
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content 