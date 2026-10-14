#!/usr/bin/env python3
"""Regenerate parsha/*.html and index.html from content/<date>-<slug>/. Run: python3 build.py"""
import json,re,pathlib,markdown,html
R=pathlib.Path(__file__).parent;T=(R/'template.html').read_text()
def md(s):
    s=re.sub(r'^\[PICTURE (\d+): (.*?)\]$',lambda m:f'<div class="pic"><div><b>PICTURE {m[1]} · COMING SOON</b>{html.escape(m[2])}</div></div>',s,flags=re.M)
    return markdown.markdown(s,extensions=['extra'])
def heb(t):
    out=[]
    for line in t.splitlines():
        m=re.match(r'^(\S+:\S+) (.*)$',line)
        if m and ':' in m[1] and re.match('[א-ת]',m[1]): out.append(f'<span class="v">{m[1]}</span>{html.escape(m[2])} ')
    return ''.join(out)
items=[]
for d in sorted((R/'content').iterdir()):
    m=json.loads((d/'meta.json').read_text());items.append(m)
    p=T
    for k,v in {**m,'hebrew_text':heb((d/'hebrew.txt').read_text()),'story':md((d/'story.md').read_text()),
                'commentary':md((d/'commentary.md').read_text()) if (d/'commentary.md').exists() else ''}.items(): p=p.replace('{{'+k+'}}',v)
    (R/'parsha'/f"{m['slug']}.html").write_text(p)
lis=''.join(f'<li><a href="parsha/{m["slug"]}.html">{m["title"]} <span lang="he">{m["hebrew"]}</span></a><br><small>{m["ref"]} · {m["date"]}</small></li>' for m in reversed(items))
(R/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Family Parsha</title><link rel="stylesheet" href="style.css"></head><body>
<header class="hero"><div class="wrap"><div class="he" lang="he">פָּרָשַׁת הַשָּׁבוּעַ</div><h1>Family Parsha</h1><p>One Torah portion a week, told for the Shabbat table · Melbourne</p></div></header>
<div class="wrap"><section><h2>Parshot</h2><ul class="list">{lis}<li class="soon">Bereshit <span lang="he">בְּרֵאשִׁית</span> · coming soon</li></ul></section>
<footer>— Rabbi Grok 🤖 (Ron's parsha bot)<br>Hebrew texts from <a href="https://www.sefaria.org">Sefaria</a> (licenses noted on each page).</footer></div></body></html>''')
print('built',len(items))
