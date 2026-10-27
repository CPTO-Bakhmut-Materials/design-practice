"""Theory illustrations for lesson 03 (logo, vector graphics)."""
import os
from common import *

L = '03-lohotyp'
LOGO = os.path.join(ROOT, 'brand-day', 'example', 'logo', 'logo.png')
LOGO_MONO = os.path.join(ROOT, 'brand-day', 'example', 'logo', 'logo-mono.png')


def logo_types():
    s = SVG(1600, 820)
    s.title('Типи логотипів', 'Приклади для вигаданих брендів')
    cards = ['Шрифтовий', 'Літерний (монограма)', 'Знак (символ)', 'Комбінований', 'Емблема']
    descs = ['лише назва', 'ініціали, 1–2 літери', 'картинка без тексту',
             'знак + назва', 'текст усередині фігури']
    for i, (h, d) in enumerate(zip(cards, descs)):
        x = 50 + i * 305
        s.rect(x, 170, 285, 470, fill=SOFT, rx=18)
        s.text(x + 142, 600, h, size=24, weight=700, anchor='middle')
        s.text(x + 142, 630, d, size=15, fill=MUTED, anchor='middle')
        cx, cy = x + 142, 390
        if i == 0:
            s.text(cx, cy + 20, 'Смаколик', size=56, family='Lobster', anchor='middle', fill='#b5482b')
        elif i == 1:
            s.circle(cx, cy, 95, fill='#1F5FAE')
            s.text(cx, cy + 34, 'ФІ', size=96, family=HEAD, weight=700, anchor='middle', fill='white')
        elif i == 2:
            s.path(f'M{cx},{cy - 110} C{cx + 110},{cy - 40} {cx + 80},{cy + 100} {cx},{cy + 110} '
                   f'C{cx - 80},{cy + 100} {cx - 110},{cy - 40} {cx},{cy - 110} Z', fill='#3AA935')
            s.path(f'M{cx},{cy - 60} L{cx},{cy + 100}', stroke='white', sw=8)
            s.path(f'M{cx},{cy + 10} L{cx + 40},{cy - 25} M{cx},{cy + 50} L{cx - 40},{cy + 15}', stroke='white', sw=8)
        elif i == 3:
            s.circle(cx - 85, cy, 45, fill='#3AA935')
            s.path(f'M{cx - 85},{cy - 30} L{cx - 85},{cy + 30} M{cx - 85},{cy} L{cx - 65},{cy - 15}', stroke='white', sw=6)
            s.text(cx - 32, cy - 4, 'Зел', size=32, family=HEAD, weight=700, fill='#2b2522')
            s.text(cx - 32, cy + 34, 'Достав', size=32, family=HEAD, weight=700, fill='#3AA935')
        else:
            s.circle(cx, cy, 120, fill='#2b2522')
            s.circle(cx, cy, 104, stroke='#f3e9dc', sw=3)
            s.text(cx, cy - 30, 'ВЕЛО', size=40, family=HEAD, weight=700, fill='#f3e9dc', anchor='middle')
            s.text(cx, cy + 22, 'ФІКС', size=40, family=HEAD, weight=700, fill='#E07A2F', anchor='middle')
            s.text(cx, cy + 66, 'з 2026 року', size=18, fill='#f3e9dc', anchor='middle')
    s.text(800, 760, 'Наш приклад «КавоБус» — комбінований логотип: знак (чашка-автобус) + шрифтова частина.',
           size=24, fill=MUTED, anchor='middle')
    return s.save(L, 'd-typy-lohotypiv')


def good_logo():
    s = SVG(1600, 900)
    s.title('Тест хорошого логотипа', 'Перевірте свій логотип за цими п’ятьма ознаками')
    s.rect(60, 170, 900, 640, fill=SOFT, rx=18)
    for w, x, y in ((560, 100, 210), (240, 100, 560), (120, 400, 600), (60, 580, 625)):
        s.image(x, y, w, w * 0.527, LOGO, preserve='xMidYMid meet')
    s.text(100, 780, 'Масштаб: 56 мм, 24 мм, 12 мм, 6 мм', size=20, fill=MUTED)
    s.image(700, 560, 220, 116, LOGO_MONO, preserve='xMidYMid meet')
    s.text(700, 700, 'Одним кольором', size=20, fill=MUTED)
    items = [('1', 'Простий', 'Мало деталей, легко запам’ятати.'),
             ('2', 'Масштабований', 'Читається і на банері, і в 2 см.'),
             ('3', 'Працює в одному кольорі', 'Печатка, гравіювання, ч/б друк.'),
             ('4', 'Доречний', 'Пасує до аудиторії (див. бриф).'),
             ('5', 'Унікальний', 'Не схожий на конкурентів.')]
    y = 210
    for n, h, d in items:
        s.circle(1015, y + 10, 24, fill=ACCENT)
        s.text(1015, y + 19, n, size=26, weight=700, fill='white', anchor='middle')
        s.text(1055, y + 18, h, size=28, weight=700)
        s.text(1055, y + 54, d, size=19, fill=MUTED)
        y += 120
    return s.save(L, 'd-test-lohotypa')


def vector_raster():
    s = SVG(1600, 820)
    s.title('Вектор і растр', 'Чому логотип малюють у векторному редакторі')
    # vector side
    s.rect(60, 170, 700, 560, fill=SOFT, rx=18)
    s.text(410, 220, 'Вектор (SVG, PDF)', size=30, weight=700, anchor='middle')
    s.circle(250, 450, 120, fill=ACCENT)
    s.rect(430, 330, 260, 260, fill='white', stroke=LINE, sw=2)
    s.add('<clipPath id="cv"><rect x="430" y="330" width="260" height="260"/></clipPath>')
    s.add(f'<g clip-path="url(#cv)"><circle cx="760" cy="760" r="480" style="fill:{ACCENT}"/></g>')
    s.line(340, 380, 430, 340, stroke=MUTED, sw=2, dash='6,6')
    s.line(340, 520, 430, 590, stroke=MUTED, sw=2, dash='6,6')
    s.rect(300, 370, 50, 50, stroke=MUTED, sw=2)
    s.text(560, 630, 'збільшення ×10: край гладкий', size=20, fill=MUTED, anchor='middle')
    s.mtext(100, 690, ['Фігури описано формулами: збільшуй скільки завгодно.'], size=20)
    # raster side
    s.rect(840, 170, 700, 560, fill=SOFT, rx=18)
    s.text(1190, 220, 'Растр (PNG, JPG)', size=30, weight=700, anchor='middle')
    s.circle(1030, 450, 120, fill=ACCENT)
    px = 26
    import math
    for iy in range(10):
        for ix in range(10):
            # sample a circle edge: centre far bottom-right
            cxp, cyp = ix + 0.5, iy + 0.5
            d = math.hypot(cxp - 18.5, cyp - 18.5)
            if d < 18.4:
                s.rect(1210 + ix * px, 330 + iy * px, px, px, fill=ACCENT)
    s.rect(1210, 330, 260, 260, stroke=LINE, sw=2)
    s.line(1120, 380, 1210, 340, stroke=MUTED, sw=2, dash='6,6')
    s.line(1120, 520, 1210, 590, stroke=MUTED, sw=2, dash='6,6')
    s.rect(1080, 370, 50, 50, stroke=MUTED, sw=2)
    s.text(1340, 630, 'збільшення ×10: видно пікселі', size=20, fill=MUTED, anchor='middle')
    s.mtext(880, 690, ['Картинка з пікселів: при збільшенні «драбинка».'], size=20)
    s.text(800, 790, 'Логотип — тільки вектор. Фото — растр. Готовий макет для друку — PDF (вектор + растр усередині).',
           size=22, fill=MUTED, anchor='middle')
    return s.save(L, 'd-vektor-rastr')


def bezier():
    s = SVG(1600, 860)
    s.title('Криві Безьє', 'Як інструмент «Перо» будує лінію')
    # main curve
    p0, c1, c2, p1, c3, c4, p2 = (140, 600), (260, 300), (480, 260), (620, 420), (760, 580), (900, 640), (1000, 380)
    s.path(f'M{p0[0]},{p0[1]} C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {p1[0]},{p1[1]} C{c3[0]},{c3[1]} {c4[0]},{c4[1]} {p2[0]},{p2[1]}',
           stroke=INK, sw=6)
    for a, b in ((p0, c1), (p1, c2), (p1, c3), (p2, c4)):
        s.line(*a, *b, stroke=BLUE, sw=2)
    for c in (c1, c2, c3, c4):
        s.circle(*c, 11, fill='white', stroke=BLUE, sw=3)
    for p in (p0, p2):
        s.add(f'<rect x="{p[0] - 11}" y="{p[1] - 11}" width="22" height="22" transform="rotate(45 {p[0]} {p[1]})" style="fill:white;stroke:{INK};stroke-width:3"/>')
    s.rect(p1[0] - 11, p1[1] - 11, 22, 22, fill='white', stroke=INK, sw=3)
    s.text(p0[0] - 20, p0[1] + 50, 'Вузол (точка)', size=22, weight=600)
    s.text(c1[0] - 120, c1[1] - 20, 'Ручка (керує вигином)', size=22, weight=600, fill=BLUE)
    s.text(p1[0] + 20, p1[1] - 20, 'Гладкий вузол', size=22, weight=600)
    s.text(780, 330, 'Сегмент', size=22, weight=600)
    s.arrow(820, 340, 820, 520, stroke=MUTED, sw=2)
    # node types
    x0 = 1100
    s.text(x0, 220, 'Типи вузлів', size=28, weight=700)
    rows = [('Кутовий (cusp)', 'ручки незалежні: гострий кут', 'M0,60 L60,0 L120,60', [(0, 60, 30, 0), (120, 60, 90, 0)]),
            ('Гладкий (smooth)', 'ручки на одній прямій', 'M0,60 C20,0 100,0 120,60', [(0, 60, 20, 0), (120, 60, 100, 0)]),
            ('Симетричний', 'ручки на прямій і однакові', 'M0,40 C30,-10 90,-10 120,40', [(0, 40, 30, -10), (120, 40, 90, -10)])]
    for i, (h, d, path, hs) in enumerate(rows):
        y = 270 + i * 170
        s.add(f'<g transform="translate({x0},{y + 40})"><path d="{path}" style="fill:none;stroke:{INK};stroke-width:5"/></g>')
        s.text(x0 + 160, y + 60, h, size=24, weight=700)
        s.text(x0 + 160, y + 92, d, size=18, fill=MUTED)
    s.mtext(140, 740, ['Клацання = кутовий вузол і пряма лінія. Клацання з протягуванням = гладкий вузол і крива.',
                       'Enter — завершити лінію, Esc — скасувати, Backspace — прибрати останній вузол.'], size=22, fill=MUTED)
    return s.save(L, 'd-kryvi-bezie')


def booleans():
    s = SVG(1600, 760)
    s.title('Логічні операції (меню Path)', 'Нижній об’єкт — квадрат, верхній — коло')
    ops = [('Union', 'Об’єднання', 'Ctrl + +'), ('Difference', 'Різниця', 'Ctrl + −'), ('Intersection', 'Перетин', 'Ctrl + *'),
           ('Exclusion', 'Виключення', 'Ctrl + ^'), ('Division', 'Ділення', 'Ctrl + /')]
    for i, (en, uk, key) in enumerate(ops):
        x = 70 + i * 300
        s.rect(x, 170, 270, 470, fill=SOFT, rx=18)
        bx, by = x + 55, 250
        sq = f'M{bx},{by} h120 v120 h-120 Z'
        cir_cx, cir_cy, r = bx + 120, by + 120, 70
        circ = (f'M{cir_cx - r},{cir_cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0 Z')
        s.add(f'<clipPath id="cs{i}"><path d="{sq}"/></clipPath><clipPath id="cc{i}"><path d="{circ}"/></clipPath>')
        if en == 'Union':
            s.path(sq, fill=ACCENT); s.path(circ, fill=ACCENT)
        elif en == 'Difference':
            s.add(f'<path d="{sq} {circ}" style="fill:{ACCENT};fill-rule:evenodd" clip-path="url(#cs{i})"/>')
        elif en == 'Intersection':
            s.add(f'<g clip-path="url(#cs{i})"><path d="{circ}" style="fill:{ACCENT}"/></g>')
        elif en == 'Exclusion':
            s.add(f'<path d="{sq} {circ}" style="fill:{ACCENT};fill-rule:evenodd"/>')
        else:
            s.path(sq, fill=ACCENT)
            s.add(f'<g clip-path="url(#cs{i})"><path d="{circ}" style="fill:#c4581c"/></g>')
            s.add(f'<g clip-path="url(#cs{i})"><path d="{circ}" style="fill:none;stroke:white;stroke-width:4"/></g>')
        s.path(sq, stroke=MUTED, sw=1.5, dash='5,5'); s.path(circ, stroke=MUTED, sw=1.5, dash='5,5')
        s.text(x + 135, 520, uk, size=28, weight=700, anchor='middle')
        s.text(x + 135, 556, en, size=20, fill=MUTED, anchor='middle')
        s.text(x + 135, 600, key, size=20, weight=600, anchor='middle')
    s.text(800, 700, 'Різниця: верхній об’єкт «вирізає» себе з нижнього. Тому важливий порядок (що вище, що нижче).',
           size=22, fill=MUTED, anchor='middle')
    return s.save(L, 'd-lohichni-operatsii')


def fill_stroke():
    s = SVG(1600, 800)
    s.title('Заливка й обведення', 'Кожна фігура має дві «фарби»')
    s.circle(220, 400, 130, fill=ACCENT, stroke=INK, sw=18)
    s.text(220, 590, 'Заливка + обведення', size=22, weight=700, anchor='middle')
    s.circle(520, 400, 130, fill=ACCENT)
    s.text(520, 590, 'Тільки заливка', size=22, weight=700, anchor='middle')
    s.circle(820, 400, 130, stroke=INK, sw=18)
    s.text(820, 590, 'Тільки обведення', size=22, weight=700, anchor='middle')
    x0 = 1060
    s.text(x0, 220, 'Кінці лінії (Cap)', size=24, weight=700)
    for i, (cap, uk) in enumerate((('butt', 'Плоский'), ('round', 'Круглий'), ('square', 'Квадратний'))):
        y = 270 + i * 60
        s.add(f'<line x1="{x0 + 20}" y1="{y}" x2="{x0 + 200}" y2="{y}" style="stroke:{INK};stroke-width:30;stroke-linecap:{cap}"/>')
        s.line(x0 + 20, y, x0 + 200, y, stroke=ACCENT, sw=2)
        s.text(x0 + 250, y + 8, uk, size=22)
    s.text(x0, 480, 'З’єднання (Join)', size=24, weight=700)
    for i, (join, uk) in enumerate((('miter', 'Гострий'), ('round', 'Круглий'), ('bevel', 'Скошений'))):
        x = x0 + i * 160
        s.add(f'<path d="M{x + 10},{620} L{x + 60},{540} L{x + 110},{620}" style="fill:none;stroke:{INK};stroke-width:24;stroke-linejoin:{join}"/>')
        s.text(x + 60, 670, uk, size=20, anchor='middle')
    s.text(60, 740, 'Пара у Fill and Stroke (Ctrl+Shift+F): вкладки Fill, Stroke paint, Stroke style.', size=22, fill=MUTED)
    return s.save(L, 'd-zalyvka-obvedennia')


def text_vs_path():
    s = SVG(1600, 700)
    s.title('Текст і контури', 'Чому перед відправкою логотип «переводять у криві»')
    s.rect(60, 170, 700, 420, fill=SOFT, rx=18)
    s.text(410, 220, 'Текстовий об’єкт', size=28, weight=700, anchor='middle')
    s.text(410, 360, 'КавоБус', size=80, family=HEAD, weight=700, anchor='middle', fill='#4A2C2A')
    s.add('<rect x="120" y="290" width="580" height="90" style="fill:none;stroke:#2f6fd6;stroke-width:2;stroke-dasharray:6,6"/>')
    s.mtext(100, 440, ['+ можна редагувати текст', '− потрібен встановлений шрифт',
                       '− на іншому ПК шрифт підміниться'], size=22)
    s.rect(840, 170, 700, 420, fill=SOFT, rx=18)
    s.text(1190, 220, 'Контур (Path)', size=28, weight=700, anchor='middle')
    s.text(1190, 360, 'КавоБус', size=80, family=HEAD, weight=700, anchor='middle', fill='#4A2C2A')
    import random
    random.seed(3)
    for x in range(905, 1480, 22):
        for y in (300, 372):
            s.rect(x + random.randint(-4, 4), y + random.randint(-6, 6), 9, 9, fill='white', stroke=BLUE, sw=2)
    s.mtext(880, 440, ['+ виглядає однаково всюди', '+ шрифт більше не потрібен', '− текст уже не відредагуєш'], size=22)
    s.text(800, 650, 'Path → Object to Path (Shift+Ctrl+C). Порада: збережіть копію з живим текстом.', size=22,
           fill=MUTED, anchor='middle')
    return s.save(L, 'd-tekst-kontury')


if __name__ == '__main__':
    for f in (logo_types, good_logo, vector_raster, bezier, booleans, fill_stroke, text_vs_path):
        print(f())
