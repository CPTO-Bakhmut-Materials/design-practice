"""Download CC0 photos from Openverse for each startup theme into brand-day/photos/."""
import json, os, sys, time, urllib.request, urllib.parse

ROOT = os.path.join(os.path.dirname(__file__), '..', 'brand-day', 'photos')
THEMES = {
    '01-kavobus': ['coffee cup', 'coffee beans', 'food truck'],
    '02-fiksit': ['computer repair', 'motherboard', 'laptop'],
    '03-zeldostav': ['vegetables', 'bicycle basket', 'fresh fruit'],
    '04-piksel-plei': ['gamepad', 'arcade', 'retro game'],
    '05-khvostyk': ['dog', 'cat', 'puppy'],
    '06-studdim': ['apartment interior', 'cozy room', 'students'],
    '07-smakolyk': ['bread', 'croissant', 'bakery'],
    '08-velofiks': ['bicycle', 'bicycle repair', 'bike wheel'],
    '09-knyhoobmin': ['books', 'library', 'bookshelf'],
    '10-fitstart': ['dumbbell', 'running', 'gym'],
    '11-linhvachat': ['conversation', 'cafe people', 'globe'],
    '12-ekoshop': ['jars', 'zero waste', 'market'],
    '13-kvitkovyi-kurier': ['flowers bouquet', 'tulips', 'roses'],
    '14-heimzona': ['keyboard gaming', 'neon', 'computer setup'],
    '15-foto-myt': ['camera', 'photographer', 'lens'],
    '16-smartkod': ['code', 'programming', 'laptop desk'],
    '17-soniachna-stantsiia': ['solar panels', 'sun', 'roof'],
    '00-fony-ta-tekstury': ['paper texture', 'wood texture', 'sky'],
}
PER_THEME = 3

def api(q):
    url = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode(
        {'q': q, 'license': 'cc0', 'size': 'large', 'page_size': 20, 'extension': 'jpg', 'mature': 'false'})
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'brand-day-workshop/1.0'}), timeout=30) as r:
        return json.load(r)['results']

HEADER = ('# Джерела фото\n\nУсі фото мають ліцензію CC0 (суспільне надбання): їх можна використовувати, змінювати й '
          'публікувати без дозволу та без зазначення автора. Джерела вказано з поваги до авторів.\n\n'
          '| Файл | Назва | Автор | Джерело | Ліцензія |\n|---|---|---|---|---|\n')
os.makedirs(ROOT, exist_ok=True)
if not os.path.exists(os.path.join(ROOT, 'CREDITS.md')):
    open(os.path.join(ROOT, 'CREDITS.md'), 'w', encoding='utf-8').write(HEADER)
for theme, queries in THEMES.items():
    d = os.path.join(ROOT, theme); os.makedirs(d, exist_ok=True)
    got = len([f for f in os.listdir(d) if f.endswith('.jpg')])
    for q in queries:
        if got >= PER_THEME: break
        try:
            res = api(q)
        except Exception as e:
            print('api fail', q, e); time.sleep(2); continue
        for r in res:
            if not r.get('width') or r['width'] < 1600 or r['height'] < 1000: continue
            name = f"{q.replace(' ', '-')}-{got + 1}.jpg"
            path = os.path.join(d, name)
            try:
                req = urllib.request.Request(r['url'], headers={'User-Agent': 'brand-day-workshop/1.0'})
                with urllib.request.urlopen(req, timeout=25) as resp, open(path, 'wb') as out:
                    out.write(resp.read())
            except Exception as e:
                print('dl fail', r['url'], e); continue
            if os.path.getsize(path) < 50_000:
                os.remove(path); continue
            with open(os.path.join(ROOT, 'CREDITS.md'), 'a', encoding='utf-8') as f:
                f.write(f"| {theme}/{name} | {(r.get('title') or '').replace('|', '/')} | {(r.get('creator') or '').replace('|', '/')} | {r.get('foreign_landing_url') or r['url']} | CC0 |\n")
            got += 1
            print(theme, name, r['width'], r['height'])
            break
        time.sleep(1)

