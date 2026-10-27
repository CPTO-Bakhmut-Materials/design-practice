"""Download picked Wikimedia CC0 photos (resized to <=3000 px) into brand-day/photos/<theme>/ and rebuild CREDITS.md."""
import json, os, subprocess, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
CAND = os.path.join(ROOT, '.sandbox', 'cand-wm')
OUT = os.path.join(ROOT, 'brand-day', 'photos')
PICKS = json.load(open(os.path.join(os.path.dirname(__file__), 'photo_picks_wm.json')))
UA = 'BrandDayWorkshop/1.0 (educational materials for a vocational college)'
HEADER = ('# Джерела фото\n\nУсі фото мають ліцензію CC0 (суспільне надбання) і взяті з Wikimedia Commons: їх можна '
          'використовувати, змінювати й публікувати без дозволу та без зазначення автора. Джерела вказано з поваги до авторів.\n\n'
          '| Файл | Назва | Автор | Джерело |\n|---|---|---|---|\n')
rows = []
for theme, picks in PICKS.items():
    meta = json.load(open(os.path.join(CAND, theme, 'meta.json')))
    d = os.path.join(OUT, theme); os.makedirs(d, exist_ok=True)
    for name, idx in picks.items():
        m = meta[idx]
        path = os.path.join(d, name + '.jpg')
        if not os.path.exists(path):
            tmp = path + '.orig'
            import time
            # originals get rate-limited first; the cached 1920 px thumbnail is a good fallback
            pre = 'https://upload.wikimedia.org/wikipedia/commons/'
            rest = m['url'][len(pre):]
            thumb = f"{pre}thumb/{rest}/1920px-{rest.split('/')[-1]}"
            for attempt in range(5):
                url = m['url'] if attempt < 2 else thumb
                r = subprocess.run(['curl', '-sfL', '--max-time', '120', '-A', UA, '-o', tmp, url])
                if r.returncode == 0:
                    break
                time.sleep(20 * (attempt + 1))
            else:
                print('FAILED', theme, name, flush=True)
                continue
            time.sleep(3)
            im = Image.open(tmp)
            im = im.convert('RGB')
            im.thumbnail((3000, 3000), Image.LANCZOS)
            im.save(path, quality=90, optimize=True)
            os.remove(tmp)
            print(theme, name, im.size, flush=True)
        rows.append(f"| {theme}/{name}.jpg | {(m['title'] or '').replace('|', '/')} | {(m['creator'] or '').replace('|', '/')} | {m['landing']} |")
open(os.path.join(OUT, 'CREDITS.md'), 'w', encoding='utf-8').write(HEADER + '\n'.join(rows) + '\n')
