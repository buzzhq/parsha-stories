#!/usr/bin/env python3
"""Regenerate parsha/*.html and index.html from content/<date>-<slug>/. Run: python3 build.py"""
import json,re,pathlib,markdown,html
R=pathlib.Path(__file__).parent;T=(R/'template.html').read_text()
def pic(slug,n,cap):
    # Real image if images/<slug>/<slug>-<n>.jpg (or .png/.webp) exists, else a 'coming soon' placeholder.
    for ext in ('jpg','png','webp'):
        if (R/'images'/slug/f'{slug}-{n}.{ext}').exists():
            c=html.escape(cap);return f'<figure class="story-img"><img src="../images/{slug}/{slug}-{n}.{ext}" alt="{c}" loading="lazy" width="1600" height="900"><figcaption>{c}</figcaption></figure>'
    return f'<div class="pic"><div><b>PICTURE {n} · COMING SOON</b>{html.escape(cap)}</div></div>'
def md(s,slug=''):
    s=re.sub(r'^\[PICTURE (\d+): (.*?)\]$',lambda m:pic(slug,m[1],m[2]),s,flags=re.M)
    return markdown.markdown(s,extensions=['extra'])
def heb(t,refs):
    out=[]
    for line in t.splitlines():
        m=re.match(r'^(\S+:\S+) (.*)$',line)
        if m and re.match('[א-ת]',m[1]):
            out.append(f'<div class="verse"><div class="ref"><span lang="en" dir="ltr">{refs.get(m[1],"")}</span> · <span lang="he">{m[1]}</span></div><p lang="he" dir="rtl">{html.escape(m[2])}</p></div>')
    return ''.join(out)
items=[]
for d in sorted((R/'content').iterdir()):
    m=json.loads((d/'meta.json').read_text());items.append(m)
    p=T
    for k,v in {**{k:v for k,v in m.items() if isinstance(v,str)},'excerpt':heb((d/'excerpt.txt').read_text(),m.get('excerpt_refs',{})),
                'story':md((d/'story.md').read_text(),m['slug']),
                'story_he':md((d/'story_he.md').read_text(),m['slug']) if (d/'story_he.md').exists() else '<p>בקרוב</p>',
                'commentary':md((d/'commentary.md').read_text()) if (d/'commentary.md').exists() else ''}.items(): p=p.replace('{{'+k+'}}',v)
    (R/'parsha'/f"{m['slug']}.html").write_text(p)
lis=''.join(f'<li><a href="parsha/{m["slug"]}.html">{m["title"]} <span lang="he">{m["hebrew"]}</span></a><br><small>{m["ref"]} · {m["date"]}</small></li>' for m in reversed(items))
(R/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Family Parsha</title><link rel="stylesheet" href="style.css"></head><body>
<header class="hero"><div class="wrap"><div class="he" lang="he">פָּרָשַׁת הַשָּׁבוּעַ</div><h1>Family Parsha</h1><p>One Torah portion a week, told for the Shabbat table · Melbourne</p></div></header>
<div class="wrap"><section><h2>Parshot</h2><ul class="list">{lis}<li class="soon">Bereshit <span lang="he">בְּרֵאשִׁית</span> · coming soon</li></ul></section>
<footer>— Rabbi Grok 🤖 (Ron's parsha bot)<br>Hebrew texts from <a href="https://www.sefaria.org">Sefaria</a> (licenses noted on each page).</footer></div></body></html>''')
print('built',len(items))
