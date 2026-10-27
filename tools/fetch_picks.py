"""Download picked candidates (full size, downscaled to <=3000 px) into brand-day/photos/<theme>/ + CREDITS.md."""
import json, os, sys, io, urllib.request
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
CAND = os.path.join(ROOT, '.sandbox', 'cand')
OUT = os.path.join(ROOT, 'brand-day', 'photos')
PICKS = json.load(open(os.path.join(os.path.dirname(__file__), 'photo_picks.json')))
HEADER = ('# Джерела фото\n\nУсі фото мають ліцензію CC0 (суспільне надбання): їх можна використовувати, змінювати й '
          'публікувати без дозволу та без зазначення автора. Джерела вказано з поваги до авторів.\n\n'
          '| Файл | Назва | Автор | Джерело |\n|---|---|---|---|\n')

rows = []
for theme, picks in PICKS.items():
    if not os.path.exists(os.path.join(CAND, theme, 'meta.json')):
        print('skip (no candidates yet)', theme); continue
    meta = json.load(open(os.path.join(CAND, theme, 'meta.json')))
    d = os.path.join(OUT, theme); os.makedirs(d, exist_ok=True)
    for name, idx in picks.items():
        m = meta[idx]
        path = os.path.join(d, name + '.jpg')
        if not os.path.exists(path):
            data = urllib.request.urlopen(urllib.request.Request(m['url'], headers={'User-Agent': 'brand-day/1.0'}), timeout=60).read()
            im = Image.open(io.BytesIO(data)).convert('RGB')
            im.thumbnail((3000, 3000), Image.LANCZOS)
            im.save(path, quality=90, optimize=True)
            print(theme, name, im.size)
        rows.append(f"| {theme}/{name}.jpg | {(m['title'] or '').replace('|', '/')} | {(m['creator'] or '').replace('|', '/')} | {m['landing']} |")
open(os.path.join(OUT, 'CREDITS.md'), 'w', encoding='utf-8').write(HEADER + '\n'.join(rows) + '\n')
