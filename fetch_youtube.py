import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────────────

YOUTUBE_API_KEY = "PASTE_YOUR_YOUTUBE_API_KEY_HERE"
ANTHROPIC_API_KEY = "PASTE_YOUR_ANTHROPIC_API_KEY_HERE"

CHANNELS = [
    {"name": "Eric Nowoslawski", "handle": "ericnowoslawski"},
    {"name": "Nick Abraham",     "handle": "nickabraham12"},
    {"name": "Matt Lucero",      "handle": "matthewlucero"},
    {"name": "Adam Erhart",      "handle": "adamerhartvideo"},
    {"name": "Aaron Shepherd",   "handle": "aaronxshepherd"},
]

VIDEOS_PER_CHANNEL = 3
OUTPUT_DIR = "research/youtube-transcripts"

# ── HELPERS ───────────────────────────────────────────────────────────────────

def get_channel_id(youtube, handle):
    res = youtube.search().list(
        part="snippet", q=handle, type="channel", maxResults=1
    ).execute()
    if res["items"]:
        return res["items"][0]["snippet"]["channelId"]
    return None

def get_recent_videos(youtube, channel_id, max_results=3):
    res = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=max_results
    ).execute()
    videos = []
    for item in res["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "date": item["snippet"]["publishedAt"][:10],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        })
    return videos

def get_full_description(youtube, video_id):
    res = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    if res["items"]:
        return res["items"][0]["snippet"]["description"]
    return ""

def get_transcript(video_id):
    # Method 1: new API style (youtube-transcript-api 1.x) with language filter
    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(video_id, languages=('en', 'en-US', 'en-GB'))
        text = " ".join([t.text for t in fetched])
        if text.strip():
            return text, "auto-generated transcript"
    except Exception as e:
        print(f"  Transcript error (method 1): {e}")

    # Method 2: new API style without language filter
    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(video_id)
        text = " ".join([t.text for t in fetched])
        if text.strip():
            return text, "auto-generated transcript"
    except Exception as e:
        print(f"  Transcript error (method 2): {e}")

    # Method 3: old API style fallback
    try:
        fetched = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en', 'en-US', 'en-GB']
        )
        text = " ".join([t["text"] for t in fetched])
        if text.strip():
            return text, "auto-generated transcript"
    except Exception as e:
        print(f"  Transcript error (method 3): {e}")

    return None, None

def structure_with_claude(title, url, date, channel_name, content, content_type):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are analyzing a YouTube video about B2B cold outreach and sales.

Video: {title}
Channel: {channel_name}
URL: {url}
Date: {date}
Content source: {content_type}

Content:
{content[:8000]}

Create a structured markdown document with these exact sections:

# {title}
**Channel:** {channel_name}
**URL:** {url}
**Date:** {date}
**Content source:** {content_type}

## Summary
2-3 sentence overview of what this video covers.

## Key Points & Strategies
- List the main actionable points and strategies discussed

## Workflows & Tools Discussed
- List any specific tools, platforms or workflows mentioned

## Use Cases Covered
- List specific use cases or examples demonstrated

## Quotes Worth Noting
- Include 1-2 direct quotes or key statements that capture the core ideas

Keep it concise, practical and focused on what someone building a
cold outreach playbook would need to know."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def save_markdown(channel_name, title, content):
    safe_channel = channel_name.lower().replace(" ", "-")
    safe_title = title[:50].lower()
    safe_title = "".join(
        c if c.isalnum() or c == "-" else "-"
        for c in safe_title.replace(" ", "-")
    )
    filename = f"{OUTPUT_DIR}/{safe_channel}_{safe_title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {filename}")

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for channel in CHANNELS:
        print(f"\nProcessing: {channel['name']}")

        channel_id = get_channel_id(youtube, channel["handle"])
        if not channel_id:
            print(f"  Could not find channel: {channel['handle']}")
            continue

        videos = get_recent_videos(youtube, channel_id, VIDEOS_PER_CHANNEL)

        for video in videos:
            print(f"  Fetching: {video['title']}")

            # Try transcript first (3 methods)
            content, content_type = get_transcript(video["video_id"])

            # Fall back to full video description
            if not content:
                print(f"  No transcript — using video description instead")
                full_desc = get_full_description(youtube, video["video_id"])
                if full_desc and len(full_desc) > 100:
                    content = full_desc
                    content_type = "video description"
                else:
                    print(f"  Description too short — skipping")
                    continue

            print(f"  Using: {content_type}")

            structured = structure_with_claude(
                video["title"],
                video["url"],
                video["date"],
                channel["name"],
                content,
                content_type
            )

            save_markdown(channel["name"], video["title"], structured)

    print("\nDone! All files saved to research/youtube-transcripts/")

if __name__ == "__main__":
    main()