# Cold Outreach Research Repository

### B2B SaaS Pipeline — Practitioner Knowledge Base

This repository contains structured research on cold outreach for B2B SaaS, collected from 10 leading practitioners across YouTube,

LinkedIn and industry blogs.

Built as part of a GTM research task using the YouTube Data API, web scraping, and Claude AI to collect, process and organize content at scale.

---

## Repository Structure

```

research/

├── [sources.md](http://sources.md)               — 10 experts with profiles and selection rationale

├── youtube-transcripts/     — 15 structured files from 5 YouTube creators

├── linkedin-posts/          — 5 structured files from 5 LinkedIn creators

└── other/                   — 5 structured blog articles from industry sources

fetch_[youtube.py](http://youtube.py)             — Automated YouTube data collection script

fetch_[blogs.py](http://blogs.py)               — Automated blog scraping and structuring script

```

---

## How the Content Was Collected

### YouTube Transcripts — Automated

Built a Python script using:

- **YouTube Data API v3** — to find channels and fetch latest videos

- **youtube-transcript-api** — to pull auto-generated transcripts

- **Anthropic API (Claude Haiku)** — to structure each transcript into

  Summary, Key Points, Workflows, Use Cases and Quotes

3 videos per creator × 5 creators = 15 structured files generated

automatically.

### LinkedIn Posts — Manual

LinkedIn has no free public API. Posts were collected manually from each creator's recent activity page. 

### Blog Articles — Automated

Built a Python scraper using:

- **requests + BeautifulSoup** — to fetch full article content

- **Anthropic API (Claude Haiku)** — to structure each article into Summary, Key Points, Data and Key Takeaway

4 articles from high-signal industry sources processed automatically.

---

## Why These 10 Experts

Selected to cover every layer of a cold outreach pipeline:

**Technical Infrastructure**

Hans Dekker — emails need to land before anything else works.

DNS, deliverability, sender reputation.

**AI and Automation at Scale**

Eric Nowoslawski, Nick Abraham — scale without losing personalization.

Claude Code, AI agents for outbound.

**Copywriting and Psychology**

Adam Erhart, Zahra Batool Butt — the message drives replies.

Frameworks, tone, personalization that feels human.

**Workflow and Tooling**

Fernando Cao Zheng, Felix Frank, Lohit Boruah — systems that make

outreach repeatable. GTM stacks, signal capture, pipeline automation.

**Pipeline and Strategy**

Aaron Shepherd, Matt Lucero — turning activity into booked meetings.

Outbound systems and measurable outcomes.

Full profiles and selection rationale in `research/sources.md`

---

## What Pattern Emerged

After reviewing content across all 10 experts and 5 blogs, one pattern stands out clearly:

The teams winning at cold outreach in 2026 are not sending more. They are testing faster, segmenting tighter, and using AI to personalize at a level that was previously impossible at scale.

Specifically:

- **Infrastructure first** — deliverability problems kill campaigns before copy ever matters

- **Signal-based targeting** — intent signals, hiring signals and technographics outperform demographic targeting alone

- **Micro-campaigns over mass blasts** — 10-20 tightly segmented campaigns beat one large generic sequence every time

- **AI as orchestration layer** — Claude Code and Clay are emerging as the central tools that connect data, personalization and sending

---

## What This Material Can Support

The collected content is strong enough to support:

- A full cold outreach playbook for a B2B SaaS product

- Sequence frameworks and copywriting guidelines

- Tool stack recommendations by use case and budget

- A/B test hypotheses based on what practitioners are actively testing

- Deliverability and infrastructure setup guidelines

- ICP segmentation and signal-based targeting frameworks

---

*Research collected April 2026*

```



