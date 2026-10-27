"""Rebuild Wikimedia candidate thumbnails from upload.wikimedia.org/…/thumb/ and contact sheets."""
import json, os, re, subprocess, urllib.request, urllib.parse, concurrent.futures as cf
ROOT = os.path.join(os.path.dirname(__file__), '..', '.sandbox', 'cand-wm')
UA = {'User-Agent': 'BrandDayWorkshop/1.0 (educational materials for a vocational college)'}


def thumb(url, w=330):
    m = re.match(r'https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$', url)
    if not m:
        return None
    a, b, name = m.groups()
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{a}/{b}/{name}/{w}px-{name}'


def get(job):
    url, path = job
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    r = subprocess.run(['curl', '-sfL', '--max-time', '30', '-A', UA['User-Agent'], '-o', path, url])
    if r.returncode:
        print('fail', path, r.returncode)
        if os.path.exists(path):
            os.remove(path)


for theme in sorted(os.listdir(ROOT)):
    d = os.path.join(ROOT, theme)
    if not os.path.isdir(d):
        continue
    if not os.path.exists(os.path.join(d, 'meta.json')):
        continue
    meta = json.load(open(os.path.join(d, 'meta.json')))
    jobs = [(thumb(m['url']), os.path.join(d, f"{m['i']:02d}.jpg")) for m in meta if thumb(m['url'])]
    import time
    for j in jobs:
        if not (os.path.exists(j[1]) and os.path.getsize(j[1]) > 1000):
            get(j); time.sleep(0.5)
    files = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
    subprocess.run(['magick', 'montage', '-label', '%t'] + [os.path.join(d, f) for f in files] +
                   ['-thumbnail', '220x150', '-geometry', '+3+3', '-tile', '8x', os.path.join(ROOT, theme + '.jpg')])
    print(theme, len(files))
