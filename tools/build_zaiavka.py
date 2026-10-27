"""Print-order form (додаток Г of plan.md): blank template + filled KavoBus example, A4 SVG.

Layer «Бланк» is locked; students type on layer «Мої відповіді» in Inkscape (like bryf-a4.svg).
Run: python3 tools/build_zaiavka.py
"""
import html, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INK, MUTED, LINE, HEAD_BG = '#3a3a3a', '#8a8277', '#b9b2a7', '#f3e9dc'
HAND = '#2f4fa8'  # «filled in» text colour

ROWS = [
    ('Назва файлу', 'rozkladka-vizytivky.pdf', 'poster-print.pdf', 'rozkladka-lystivky.pdf'),
    ('Формат після обрізу, мм', '90 × 50', '210 × 297 (A4)', '148 × 210 (A5)'),
    ('Виліт, мм', '2', '3', '3'),
    ('Аркуш друку / виробів на аркуші', 'A4 / 10', 'A4 / 1', 'SRA4 / 2'),
    ('Кольоровість (4+4, 4+0, 1+0)', '4+4', '4+0', '4+4'),
    ('Папір (тип, щільність г/м²)', 'крейд. мат. 350', 'крейд. глянц. 170', 'крейд. мат. 130'),
    ('Тираж, шт.', '100', '10', '200'),
    ('Післядрукарське оброблення', 'порізка', '—', 'порізка'),
    ('Орієнтовна вартість, грн', '250', '250', '600'),
]
HEADER = [('Замовник (ПІБ)', 'Олена Коваленко'), ('Бренд', '«КавоБус»'), ('Телефон / e-mail', '+380 67 000 00 00'),
          ('Дата', '20.10.2026')]
CHECK = ['PDF/X-4, шрифти вбудовані або в кривих', 'Вильоти з усіх боків, мітки обрізу',
         'Зображення не менше 300 dpi', 'Кольори перевірено екранною кольоропробою (CMYK)',
         'Важливий текст у безпечній зоні', 'Назви файлів латиницею, без пробілів']


def t(x, y, s, size=3.4, weight='normal', fill=INK, anchor='start'):
    return (f'<text x="{x}" y="{y}" style="font-family:Montserrat;font-weight:{weight};font-size:{size}px;'
            f'fill:{fill};text-anchor:{anchor}">{html.escape(s)}</text>')


def build(filled):
    form, ans = [], []
    form.append(t(15, 25, 'ЗАЯВКА ДО ДРУКАРНІ', 10, 'bold'))
    form.append(t(15, 33, 'Бланк замовлення поліграфії (додаток Г)', 4.2, fill=MUTED))
    y = 46
    for label, val in HEADER:
        form.append(t(15, y, label.upper(), 3, 'bold'))
        form.append(f'<line x1="60" y1="{y + 1}" x2="195" y2="{y + 1}" style="stroke:{LINE};stroke-width:0.3"/>')
        ans.append(t(62, y - 0.5, val, 4, fill=HAND))
        y += 9
    # table
    x = [15, 75, 115, 155, 195]
    y0, rh = y + 6, 11
    form.append(f'<rect x="15" y="{y0}" width="180" height="{rh}" style="fill:{HEAD_BG}"/>')
    for i, h in enumerate(('Поле', 'Візитівки', 'Плакат', 'Листівки')):
        form.append(t(x[i] + 2.5, y0 + 7, h, 3.6, "bold"))
    for r, row in enumerate(ROWS):
        yy = y0 + rh * (r + 1)
        words, lines, cur = row[0].split(), [], ''
        for w in words:
            if len(cur + ' ' + w) > 28:
                lines.append(cur); cur = w
            else:
                cur = (cur + ' ' + w).strip()
        lines.append(cur)
        for k, s in enumerate(lines):
            form.append(t(x[0] + 2.5, yy + 4.8 + k * 3.6, s, 3.0))
        for c in range(3):
            ans.append(t(x[c + 1] + 2, yy + 7, row[c + 1], 3.0, fill=HAND))
    y1 = y0 + rh * (len(ROWS) + 1)
    for xx in x:
        form.append(f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y1}" style="stroke:{LINE};stroke-width:0.3"/>')
    for r in range(len(ROWS) + 2):
        yy = y0 + rh * r
        form.append(f'<line x1="15" y1="{yy}" x2="195" y2="{yy}" style="stroke:{LINE};stroke-width:0.3"/>')
    # total + checklist
    y = y1 + 12
    form.append(t(15, y, 'РАЗОМ, ГРН', 3.4, 'bold'))
    form.append(f'<line x1="60" y1="{y + 1}" x2="120" y2="{y + 1}" style="stroke:{LINE};stroke-width:0.3"/>')
    ans.append(t(62, y - 0.5, '1100', 4, 'bold', HAND))
    y += 14
    form.append(t(15, y, 'ПЕРЕД ВІДПРАВЛЕННЯМ ПЕРЕВІРЕНО', 3.4, 'bold'))
    for i, s in enumerate(CHECK):
        yy = y + 8 + i * 7
        form.append(f'<rect x="15" y="{yy - 3.6}" width="4.2" height="4.2" style="fill:none;stroke:{INK};stroke-width:0.3"/>')
        form.append(t(22, yy, s, 3.4))
        ans.append(t(15.6, yy + 0.2, '✓', 4.4, 'bold', HAND))
    form.append(t(15, 287, 'Ціни в прикладі умовні, для навчальної вправи. Справжні ціни й вимоги до файлів уточнюйте в друкарні.',
                  2.6, fill=MUTED))
    answers = ''.join(ans) if filled else ''
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<svg width="210mm" height="297mm" viewBox="0 0 210 297" version="1.1" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns="http://www.w3.org/2000/svg">\n'
            '<title>Заявка до друкарні</title><sodipodi:namedview pagecolor="#ffffff" inkscape:document-units="mm"/>\n'
            f'<g inkscape:groupmode="layer" inkscape:label="Бланк" sodipodi:insensitive="true">{"".join(form)}</g>\n'
            f'<g inkscape:groupmode="layer" inkscape:label="Мої відповіді">{answers}</g>\n</svg>\n')


if __name__ == '__main__':
    out = [(os.path.join(ROOT, 'brand-day', 'templates', 'zaiavka-a4.svg'), False),
           (os.path.join(ROOT, 'brand-day', 'example', 'print', 'zaiavka.svg'), True)]
    for path, filled in out:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(build(filled))
        print(path)
