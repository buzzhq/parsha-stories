# Family Parsha site
Plain static HTML for GitHub Pages (`.nojekyll`, no build needed on the server).

## Add a new week
1. Copy `content/2026-10-17-noach/` to `content/<YYYY-MM-DD>-<slug>/`.
2. Replace `excerpt.txt` (4-6 story-rich verses, one per line: `ו:ט <text>`, copied exactly from Sefaria), `story.md` (English), `story_he.md` (Hebrew story, rendered RTL), `commentary.md`, and edit `meta.json` (slug, title, hebrew, ref, date, source/license, `sefaria_he`/`sefaria_bi` full-text links, `excerpt_refs` mapping Hebrew refs to English labels).
   Page order: Torah excerpt → English → עברית → Commentary.
3. Picture placeholders in markdown: a line `[PICTURE 1: caption]`.
4. Run `python3 build.py` (needs `pip install markdown`). It writes `parsha/<slug>.html` and refreshes `index.html`.
5. Commit the generated files and push.
