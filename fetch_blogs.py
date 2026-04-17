import os
import re
import requests
from bs4 import BeautifulSoup
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = "PASTE_YOUR_ANTHROPIC_API_KEY_HERE"

BLOGS = [
    {
        "url": "https://databar.ai/blog/article/cold-email-in-2026-how-claude-code-is-changing-outbound-strategy",
        "title": "Cold Email in 2026 — How Claude Code Is Changing Outbound Strategy",
        "source": "Databar.ai"
    },
    {
        "url": "https://www.clay.com/blog/eric-nowoslawski-cold-email-tips",
        "title": "Eric Nowoslawski Cold Email Tips",
        "source": "Clay.com"
    },
    {
        "url": "https://martal.ca/b2b-cold-email-statistics-lb/",
        "title": "B2B Cold Email Statistics 2026 — Benchmarks and What Works Now",
        "source": "Martal.ca"
    },
    {
        "url": "https://sopro.io/resources/blog/cold-outreach-statistics/",
        "title": "Cold Outreach Statistics 2026",
        "source": "Sopro.io"
    },
    {
        "url": "https://instantly.ai/blog/cold-email-sequence/",
        "title": "Cold Email Sequence Guide",
        "source": "Instantly.ai"
    },
]

OUTPUT_DIR = "research/other"

# ── HELPERS ───────────────────────────────────────────────────────────────────

def fetch_blog_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "nav", "footer",
                         "header", "aside", "form", "iframe"]):
            tag.decompose()

        # Try to get main content
        main = (
            soup.find("article") or
            soup.find("main") or
            soup.find(class_=re.compile(r"post|content|article|blog", re.I)) or
            soup.find("body")
        )

        text = main.get_text(separator="\n", strip=True) if main else ""

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(lines)

        return text[:8000] if text else None

    except Exception as e:
        print(f"  Fetch error: {e}")
        return None

def structure_with_claude(title, url, source, content):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are analyzing a blog post about B2B cold outreach and sales.

Title: {title}
Source: {source}
URL: {url}

Content:
{content}

Create a structured markdown document with these exact sections:

# {title}
**Source:** {source}
**URL:** {url}
**Collected:** April 2026

## Summary
2-3 sentence overview of what this article covers.

## Key Points & Strategies
- List the main actionable points and strategies discussed

## Data & Statistics
- List any specific numbers, benchmarks or statistics mentioned

## Tools & Platforms Referenced
- List any specific tools or platforms mentioned

## Key Takeaway
One sentence capturing the single most important insight from this article.

Keep it concise and focused on what someone building a cold outreach
playbook would need to know."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def save_markdown(source, title, content):
    safe_source = source.lower().replace(" ", "-").replace(".", "-")
    safe_title = title[:50].lower()
    safe_title = "".join(
        c if c.isalnum() or c == "-" else "-"
        for c in safe_title.replace(" ", "-")
    )
    filename = f"{OUTPUT_DIR}/{safe_source}_{safe_title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {filename}")

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for blog in BLOGS:
        print(f"\nProcessing: {blog['title']}")
        print(f"  Fetching: {blog['url']}")

        content = fetch_blog_content(blog["url"])

        if not content or len(content) < 200:
            print(f"  Could not fetch enough content — skipping")
            continue

        print(f"  Fetched {len(content)} characters")
        print(f"  Structuring with Claude...")

        structured = structure_with_claude(
            blog["title"],
            blog["url"],
            blog["source"],
            content
        )

        save_markdown(blog["source"], blog["title"], structured)

    print("\nDone! All files saved to research/other/")

if __name__ == "__main__":
    main()
