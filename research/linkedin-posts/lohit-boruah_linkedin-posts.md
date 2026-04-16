# Lohit Boruah — LinkedIn Posts
**Profile:** https://www.linkedin.com/in/yourvibeguy/
**Collected:** April 2026

---

## Post 1 — Full Outbound Pipeline with Claude Code + Icypeas

**Theme:** AI-orchestrated outbound pipeline using Claude Code and Icypeas API

You can now build a full outbound pipeline with just Claude Code
and Icypeas. Here's how the whole thing works:

**Step 1** — Define your ICP in a simple JSON config. Role, industry,
company size, geography, whatever signals matter to you.

**Step 2** — Claude Code parses that config and builds an
Icypeas-compatible search query. No manual filters. It reads your
intent and structures the payload.

**Step 3** — Icypeas pulls matching prospects through
`/v1/prospects/search`. Raw lead objects come back.

**Step 4** — For each lead, Claude Code loops through two Icypeas
endpoints:
- `/v1/prospects/enrich` for emails, company data, LinkedIn profiles
- `/v1/email/verify` to check deliverability
- Invalid emails get dropped automatically

**Step 5** — Claude Code cleans what's left. Deduplicates, normalizes
fields, scores every lead by ICP fit and role seniority.

**Step 6** — Claude Code writes personalized first lines and full cold
email drafts based on each lead's context. Not templates. Actual
contextual copy.

**Step 7** — Export. CSV or JSON, ready for your campaign tool.

**Key insight:** Claude Code handles the orchestration — the thinking,
the logic, the loops, the writing. Icypeas handles the data — prospect
search, enrichment, and email verification. ICP config goes in.
Campaign-ready leads come out.

---

## Post 2 — Turning LinkedIn Engagement Into Pipeline

**Theme:** Converting post engagement signals into outbound pipeline

Every post that gets likes, comments, or profile views is literally
showing you who's paying attention — but without a system, all of
that intent disappears into notifications.

**The system:**
- Publish with intent so the right people feel pulled to engage
- Capture every interaction as a signal instead of treating it as vanity
- Enrich and filter signals to focus only on ICP-matched people
- Activate outreach based on what they engaged with so it feels like
  a natural continuation, not a cold interruption
- Convert with structure — make it easy to book, reply, or continue

**The stack:**

Capture:
- Apify / PhantomBuster

Enrichment:
- Prospeo (primary, fast + accurate emails)
- Clay (orchestration + scoring)
- Icypeas / LeadMagic (backup coverage)

Activation:
- Smartlead / Instantly.ai
- Aimfox / salesrobots

Conversion:
- Calendly
- HubSpot / Attio

Nurture:
- beehiiv

**Key insight:** Tools don't make this work. Routing logic does.
Only three things matter: Replies, Conversations, Meetings booked.
Everything else is noise. Build the loop once and every post starts
compounding.

---

## Post 3 — Company Size Segmentation Experiment

**Theme:** How company size affects cold email reply rates

Ran a small experiment for a client. Launched 4 campaigns across
2 different industries. For each industry: 2 campaigns with 3
different variations, segmented into 11–50 employees and 50–100
employees. Same offer, same variation — only difference was company
size.

**Result:** In each industry, the campaign targeting one company size
clearly outperformed the other. Better replies. Better intent. Better
conversations.

**Key insight:** Same offer, same copy — different company size
produced meaningfully different results. Segmenting by company size
is not optional. It directly affects how prospects react to the same
message. Test company size as a variable before testing anything else.
