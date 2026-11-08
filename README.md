# Twin Angels

A TikTok-style news feed that teaches how the world works: politics, international relations, economy, finance, tech, energy, media and arts, and how each one moves the others.

**Live:** [taapp.nur.capital](https://taapp.nur.capital) — open on a phone, then Share → Add to Home Screen.

## What a story looks like
Every story is a vertical post you swipe through sideways:

1. **Cover** with a chart built only from sourced numbers
2. **Basics first** — the 2–3 things a newcomer must know before the story makes sense
3. **Who's involved** — an animated map of the actors and what they do to each other
4. **Mechanism** — cause → effect, each link marked *fact* or *inference*, with a plain "why"
5. **Terms** that go into a spaced-repetition deck
6. **Where it hits** — chains showing how the event travels into other spheres
7. **Quiz** with an explanation for every option, plus a yes/no prediction
8. **Explain it yourself** — write the logic in your own words

After the news, the feed keeps going with 120 evergreen "how it works" cards and review rounds.

## Learning techniques built in
Retrieval practice, spaced repetition (1/3/7/14/30/60 days), the generation effect ("what happens next?"), interleaving across spheres, dual coding (diagram + text), elaboration via historical analogies, and calibrated predictions. Every abbreviation and term is tappable for a plain-language explanation (246-entry glossary).

## How it's built
- `app/index.html` — the whole app in one file: vanilla JS, inline SVG charts, no build step, no framework.
- `app/editions/` — daily editions (JSON), `app/library/` — evergreen cards, `app/glossary.json`.
- `editions/SCHEMA.md` — the content schema. Every fact carries a dated source; mechanism steps are tagged fact or inference.
- `.claude/skills/brief/` — the editorial pipeline: Claude Code researches the day's news with parallel agents, decomposes each story, validates it (`scripts/build_edition.py`) and republishes.
- `scripts/site_zip.py` — builds the static, installable (PWA) version for any host.

On claude.ai the app also syncs progress, lets you ask Claude about a story, grades your own explanations and checks predictions against what happened. On static hosting those features hide and progress stays in the browser.

## Run locally
```bash
python3 scripts/dev_page.py
python3 -m http.server 8765 --directory app
```
Then open http://localhost:8765/dev.html.

## Content note
News summaries are written from public sources linked in every story. Not investment advice.
