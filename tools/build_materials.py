"""Download/preview page for the student materials (brand-day/).

Writes lessons/01-vstup/materialy.md and the generated folder lessons/01-vstup/materialy/:
  brand-day -> ../../../brand-day   (symlink; mdBook copies it into the book)
  zip/      brand-day.zip + one archive per top-level folder (paths rooted at brand-day/)
  prev/     thumbnails (photos, PNG, SVG, PDF first page, .kra merged image)
Run locally before `mdbook build` and commit the result (Inkscape/poppler/Pillow are only needed here);
zip/ is not committed: `--zips` rebuilds only the archives (stdlib only, used by the Pages workflow).
Unchanged files are skipped.
"""
import html, io, os, re, subprocess, sys, zipfile

sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'brand-day')
LESSON = os.path.join(ROOT, 'lessons', '01-vstup')
OUT = os.path.join(LESSON, 'materialy')
PAGE = os.path.join(LESSON, 'materialy.md')
URL = 'materialy'  # OUT relative to the page
THUMB_W = 480

FOLDERS = [
    ('fonts', 'Шрифти', '8 безкоштовних шрифтів із підтримкою української (ліцензія SIL OFL).'),
    ('photos', 'Фото', 'Фото з ліцензією CC0 за темами стартапів. Відкрийте теку свого стартапу й теку фонів.'),
    ('templates', 'Шаблони', 'Бланки брифу, мудборду й заявки до друкарні, шаблон візитівки, шаблони розкладки.'),
    ('icc', 'Колірний профіль', 'ICC-профіль друку FOGRA39 для екранної кольоропроби в Krita і Scribus.'),
    ('mockups', 'Мокапи', 'Шаблони мокапів для презентації. Файли PNG поруч — заглушки, які ви заміните своїми дизайнами.'),
    ('example', 'Приклад «КавоБус»', 'Готовий бренд, зроблений за цими уроками: логотип, візитівка, ключовий візуал, плакат, листівка, файли для друку.'),
]
IMG = {'.jpg', '.jpeg', '.png'}
HINT = {'.sla': 'Відкрийте в Scribus', '.kra': 'Відкрийте в Krita', '.icc': 'Колірний профіль',
        '.svg': 'Відкрийте в Inkscape', '.txt': 'Текст ліцензії', '.ttf': 'Шрифт'}
NOTES = {'templates/vizytivka-90x50.svg': 'Порожній: 2 сторінки, виліт 2 мм, поля 4 мм'}
SAMPLE = 'Бренд за день — Ґґ Єє Її Щщ 0123'


def size(n):
    for unit, k in (('ГБ', 1 << 30), ('МБ', 1 << 20), ('КБ', 1 << 10)):
        if n >= k:
            return f'{n / k:.1f}'.replace('.', ',').replace(',0', '') + ' ' + unit
    return f'{n} Б'


def fresh(dst, *srcs):
    return os.path.exists(dst) and all(os.path.getmtime(dst) >= os.path.getmtime(s) for s in srcs)


def files(folder):
    base = os.path.join(SRC, folder)
    out = []
    for d, dirs, names in os.walk(base):
        dirs.sort()
        out += [os.path.relpath(os.path.join(d, n), SRC) for n in sorted(names) if not n.startswith('.')]
    return out


# --- archives ------------------------------------------------------------------
def build_zip(name, rels):
    dst = os.path.join(OUT, 'zip', name + '.zip')
    srcs = [os.path.join(SRC, r) for r in rels]
    if not fresh(dst, *srcs):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        tmp = dst + '.part'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for r, s in zip(rels, srcs):
                packed = os.path.splitext(r)[1].lower() in IMG | {'.kra'}
                z.write(s, os.path.join('brand-day', r), zipfile.ZIP_STORED if packed else zipfile.ZIP_DEFLATED)
        os.replace(tmp, dst)
        print('zip', os.path.relpath(dst, ROOT))
    return f'{URL}/zip/{name}.zip', os.path.getsize(dst)


# --- thumbnails ----------------------------------------------------------------
def thumb(rel):
    """Return the thumbnail URL for rel, or None if the type has no preview."""
    src = os.path.join(SRC, rel)
    ext = os.path.splitext(rel)[1].lower()
    if ext not in IMG | {'.svg', '.pdf', '.kra'}:
        return None
    photo = ext in ('.jpg', '.jpeg')
    out_rel = os.path.join('prev', os.path.splitext(rel)[0] + ('.jpg' if photo else '.png'))
    dst = os.path.join(OUT, out_rel)
    if not fresh(dst, src):
        from PIL import Image
        import cap
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if ext in IMG:
            im = Image.open(src)
        elif ext == '.kra':
            with zipfile.ZipFile(src) as z:
                im = Image.open(io.BytesIO(z.read('mergedimage.png')))
        elif ext == '.pdf':
            png = subprocess.run(['pdftoppm', '-png', '-singlefile', '-f', '1', '-scale-to', str(THUMB_W * 2), src],
                                 check=True, capture_output=True).stdout
            im = Image.open(io.BytesIO(png))
        else:  # svg: render with Inkscape in the sandbox profile (bundled fonts)
            cap.run('inkscape', src, '--export-type=png', f'--export-width={THUMB_W * 2}',
                    '--export-background=white', '--export-background-opacity=1', f'--export-filename={dst}')
            im = Image.open(dst)
        im.thumbnail((THUMB_W, THUMB_W * 2))
        if photo:
            im.convert('RGB').save(dst, quality=82, optimize=True)
        else:
            im.save(dst, optimize=True)
        print('prev', out_rel)
    return f'{URL}/{out_rel}'


# --- page ----------------------------------------------------------------------
def credits():
    """photos/CREDITS.md table: 'folder/file.jpg' -> (author, source url)."""
    out = {}
    for line in open(os.path.join(SRC, 'photos', 'CREDITS.md'), encoding='utf-8'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 4 and cells[3].startswith('http'):
            out[cells[0]] = (cells[2], cells[3])
    return out


def card(rel, label=None, note=None):
    href = f'{URL}/brand-day/{rel}'
    ext = os.path.splitext(rel)[1].lower()
    name = html.escape(label or os.path.basename(rel))
    t = thumb(rel)
    if t:
        top = f'<a class="mat-thumb" href="{href}" target="_blank"><img src="{t}" alt="{name}" loading="lazy"></a>'
    else:
        top = (f'<div class="mat-thumb mat-none"><span>{ext[1:].upper()}</span>'
               f'<small>{HINT.get(ext, "")}</small></div>')
    meta = f'{size(os.path.getsize(os.path.join(SRC, rel)))} · <a href="{href}" download>Завантажити</a>'
    note = note or NOTES.get(rel)
    note = f'<span class="mat-note">{note}</span>' if note else ''
    return f'<figure class="mat-card">{top}<figcaption><span class="mat-name">{name}</span>{note}<span class="mat-meta">{meta}</span></figcaption></figure>'


def lead(text, button):
    """Sentence + download button side by side (table used for layout only)."""
    return (f'<table class="mat-lead" role="presentation"><tr><td>{text}</td>'
            f'<td class="mat-lead-btn">{button}</td></tr></table>')


def grid(cards):
    return '<div class="mat-grid">\n' + '\n'.join(cards) + '\n</div>'


def fonts_block(rels):
    faces, rows = [], []
    for fam in sorted({r.split('/')[1] for r in rels}):
        fr = [r for r in rels if r.split('/')[1] == fam and r.endswith('.ttf')]
        cells = []
        for r in fr:
            style = os.path.splitext(os.path.basename(r))[0].split('-', 1)[1]
            css = f'mat-{fam}-{style}'
            faces.append(f"@font-face {{ font-family: '{css}'; src: url('{URL}/brand-day/{r}'); }}")
            cells.append(f'<div class="mat-font-row"><span class="mat-font-sample" style="font-family: \'{css}\'">{SAMPLE}</span>'
                         f'<span class="mat-meta">{style} · {size(os.path.getsize(os.path.join(SRC, r)))} · '
                         f'<a href="{URL}/brand-day/{r}" download>Завантажити</a></span></div>')
        lic = f'fonts/{fam}/OFL.txt'
        rows.append(f'<div class="mat-font"><div class="mat-font-head"><b>{fam}</b>'
                    f'<a href="{URL}/brand-day/{lic}" target="_blank">Ліцензія OFL</a></div>' + ''.join(cells) + '</div>')
    return '<style>\n' + '\n'.join(faces) + '\n</style>\n\n' + '\n'.join(rows)


def photos_block(rels):
    cr = credits()
    parts = []
    by_dir = {}
    for r in rels:
        if r.endswith('.jpg'):
            by_dir.setdefault(r.split('/')[1], []).append(r)
    for d, rs in by_dir.items():
        cards = []
        for r in rs:
            a = cr.get(r.split('/', 1)[1])
            note = f'Автор: <a href="{html.escape(a[1])}" target="_blank">{html.escape(a[0])}</a>' if a else None
            cards.append(card(r, note=note))
        opened = ' open' if d.startswith('00-') else ''
        zurl, zsize = build_zip(f'photos-{d}', files(f'photos/{d}'))
        parts.append(f'<details class="mat-group" id="photos-{d}"{opened}><summary><code>{d}/</code> · {len(rs)} фото · '
                     f'<a href="{zurl}" download>{d}.zip ({size(zsize)})</a></summary>\n'
                     + grid(cards) + '\n</details>')
    return (f'Джерела й автори всіх фото — у файлі [`photos/CREDITS.md`]({URL}/text/photos/CREDITS.txt).\n\n'
            + '\n'.join(parts))


def zips():
    """All archives the page links to: brand-day.zip, one per folder, one per photo theme."""
    build_zip('brand-day', [r for f, _, _ in FOLDERS for r in files(f)])
    for folder, _, _ in FOLDERS:
        build_zip(folder, files(folder))
    for d in sorted(os.listdir(os.path.join(SRC, 'photos'))):
        if os.path.isdir(os.path.join(SRC, 'photos', d)):
            build_zip(f'photos-{d}', files(f'photos/{d}'))


def main():
    os.makedirs(OUT, exist_ok=True)
    link = os.path.join(OUT, 'brand-day')
    if not os.path.islink(link):
        os.symlink(os.path.relpath(SRC, OUT), link)

    # mdBook does not copy .md files: serve them as UTF-8 text (BOM so browsers pick the encoding)
    for rel in (r for f, _, _ in FOLDERS for r in files(f) if r.endswith('.md')):
        dst = os.path.join(OUT, 'text', rel[:-3] + '.txt')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8-sig').write(open(os.path.join(SRC, rel), encoding='utf-8').read())

    every = [r for f, _, _ in FOLDERS for r in files(f)]
    all_url, all_size = build_zip('brand-day', every)
    md = ['# Матеріали воркшопу', '',
          '[← До уроку](README.md)', '',
          lead('Тут можна переглянути й завантажити всі файли теки <code>brand-day/</code>.',
               f'<a class="mat-button" href="{all_url}" download>brand-day.zip ({size(all_size)})</a>'), '',
          'Розпакуйте архів у свою теку користувача: з’явиться тека `brand-day/` з усіма підтеками. '
          'Архів окремої теки розпаковуйте туди ж — файли потраплять у `brand-day/` на свої місця.', '',
          'Клацніть прев’ю, щоб відкрити файл у браузері (PDF, зображення, SVG). '
          'Файли Krita (`.kra`) і Scribus (`.sla`) браузер не відкриває: їх треба завантажити.', '']
    for folder, title, desc in FOLDERS:
        rels = files(folder)
        zurl, zsize = build_zip(folder, rels)
        md += [f'## {title}: `{folder}/` {{#{folder}}}', '',
               lead(desc, f'<a class="mat-button mat-button-small" href="{zurl}" download>{folder}.zip ({size(zsize)})</a>'), '']
        if folder == 'fonts':
            md.append(fonts_block(rels))
        elif folder == 'photos':
            md.append(photos_block(rels))
        else:
            md.append(grid(card(r, label=r.split('/', 1)[1]) for r in rels))
        md.append('')
    md += ['[← До уроку](README.md)', '',
           # links from lessons point at a photo group: open it
           '<script>(function () { var d = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));'
           ' if (d && d.tagName === "DETAILS") d.open = true; })();</script>', '']
    open(PAGE, 'w', encoding='utf-8').write('\n'.join(md))
    print('page', os.path.relpath(PAGE, ROOT))


if __name__ == '__main__':
    zips() if '--zips' in sys.argv else main()
