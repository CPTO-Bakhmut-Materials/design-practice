"""Fetch CC0 photo candidates (StockSnap/rawpixel via Openverse), build a numbered contact sheet per theme."""
import json, os, subprocess, urllib.request, urllib.parse, concurrent.futures as cf

ROOT = os.path.join(os.path.dirname(__file__), '..', '.sandbox', 'cand')
THEMES = {
    '01-kavobus': ['coffee cup', 'coffee beans', 'food truck', 'latte'],
    '02-fiksit': ['computer repair', 'smartphone', 'laptop'],
    '03-zeldostav': ['vegetables', 'bicycle city', 'groceries'],
    '04-piksel-plei': ['game controller', 'gaming'],
    '05-khvostyk': ['dog', 'cat'],
    '06-studdim': ['apartment', 'living room', 'students'],
    '07-smakolyk': ['bread', 'croissant', 'pastry'],
    '08-velofiks': ['bicycle', 'bike repair'],
    '09-knyhoobmin': ['books', 'reading'],
    '10-fitstart': ['fitness', 'dumbbell', 'running'],
    '11-linhvachat': ['conversation', 'friends', 'travel'],
    '12-ekoshop': ['jars', 'market', 'vegetables market'],
    '13-kvitkovyi-kurier': ['flowers', 'bouquet'],
    '14-heimzona': ['gaming', 'headphones', 'keyboard'],
    '15-foto-myt': ['camera', 'photographer'],
    '16-smartkod': ['code', 'programming', 'laptop desk'],
    '17-soniachna-stantsiia': ['solar panels', 'sun', 'roof'],
    '00-fony-ta-tekstury': ['texture', 'paper', 'wood', 'sky'],
    '99-mokapy': ['blank wall', 'white wall', 'desk top view', 'white table'],
}


def api(q):
    url = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode(
        {'q': q, 'license': 'cc0', 'source': 'stocksnap', 'page_size': 8, 'mature': 'false'})
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'brand-day/1.0'}), timeout=30) as r:
        return json.load(r)['results']


def get(url, path):
    if os.path.exists(path):
        return
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'brand-day/1.0'}), timeout=30) as r:
        open(path, 'wb').write(r.read())


for theme, queries in THEMES.items():
    d = os.path.join(ROOT, theme); os.makedirs(d, exist_ok=True)
    meta, jobs = [], []
    for q in queries:
        try:
            res = api(q)
        except Exception as e:
            print('api fail', q, e); continue
        for r in res:
            i = len(meta)
            meta.append({'i': i, 'q': q, 'url': r['url'], 'title': r.get('title'), 'creator': r.get('creator'),
                         'landing': r.get('foreign_landing_url'), 'w': r.get('width'), 'h': r.get('height')})
            jobs.append((r['thumbnail'], os.path.join(d, f'{i:02d}.jpg')))
    with cf.ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda j: get(*j) if True else None, jobs))
    json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
    files = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
    subprocess.run(['magick', 'montage', '-label', '%t'] + [os.path.join(d, f) for f in files] +
                   ['-thumbnail', '220x150', '-geometry', '+3+3', '-tile', '8x', os.path.join(ROOT, theme + '.jpg')])
    print(theme, len(meta))
