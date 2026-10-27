"""Theory illustrations for lesson 02 (brief, colour, typography)."""
import math
from common import *

L = '02-bryf-i-mudbord'

WHEEL = [  # traditional RYB artist wheel, clockwise from top
    ('#FFD400', 'Жовтий', 'P'), ('#FFA800', 'Жовто-помаранчевий', 'T'), ('#FF7A00', 'Помаранчевий', 'S'),
    ('#F2451D', 'Червоно-помаранчевий', 'T'), ('#E2231A', 'Червоний', 'P'), ('#B5196E', 'Червоно-фіолетовий', 'T'),
    ('#6A2C91', 'Фіолетовий', 'S'), ('#3F3C9C', 'Синьо-фіолетовий', 'T'), ('#1F5FAE', 'Синій', 'P'),
    ('#0F8C8C', 'Синьо-зелений', 'T'), ('#3AA935', 'Зелений', 'S'), ('#A6CE39', 'Жовто-зелений', 'T'),
]


def sector(cx, cy, r1, r2, a1, a2):
    def p(r, a):
        return cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a))
    x1, y1 = p(r2, a1); x2, y2 = p(r2, a2); x3, y3 = p(r1, a2); x4, y4 = p(r1, a1)
    return f'M{x1:.1f},{y1:.1f} A{r2},{r2} 0 0 1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A{r1},{r1} 0 0 0 {x4:.1f},{y4:.1f} Z'


def wheel(s, cx, cy, r, inner=0.45, marks=(), gap=1.2):
    for i, (c, _, _) in enumerate(WHEEL):
        a = i * 30 - 15
        s.path(sector(cx, cy, r * inner, r, a + gap / 2, a + 30 - gap / 2), fill=c)
    for i in marks:
        a = math.radians(i * 30)
        x, y = cx + r * 0.73 * math.sin(a), cy - r * 0.73 * math.cos(a)
        s.circle(x, y, r * 0.11, fill='white', stroke=INK, sw=3)
    return s


def color_wheel():
    s = SVG(1600, 900)
    s.title('Колірне коло', 'Основа для підбору гармонійних кольорів')
    cx, cy, r = 480, 500, 330
    wheel(s, cx, cy, r, inner=0.42)
    for i, (c, name, kind) in enumerate(WHEEL):
        a = math.radians(i * 30)
        x, y = cx + r * 0.71 * math.sin(a), cy - r * 0.71 * math.cos(a)
        rr = {'P': 30, 'S': 22, 'T': 0}[kind]
        if rr:
            s.circle(x, y, rr, fill='white', stroke=INK, sw=3)
            s.text(x, y + rr * 0.38, {'P': '1', 'S': '2'}[kind], size=rr * 1.05, weight=700, anchor='middle')
    lx = 950
    rows = [('P', 'Основні (первинні)', 'Червоний, жовтий, синій. Їх не можна отримати змішуванням.'),
            ('S', 'Похідні (вторинні)', 'Помаранчевий, зелений, фіолетовий: суміш двох основних.'),
            ('T', 'Третинні', 'Суміш основного й сусіднього похідного кольору.')]
    y = 250
    for kind, head, desc in rows:
        cols = [c for c, _, k in WHEEL if k == kind]
        for j, c in enumerate(cols[:6]):
            s.rect(lx + j * 46, y, 38, 38, fill=c, rx=6)
        s.text(lx, y + 80, head, size=30, weight=700)
        words = desc.split(' ')
        lines, cur = [], ''
        for w in words:
            if len(cur + ' ' + w) > 38:
                lines.append(cur); cur = w
            else:
                cur = (cur + ' ' + w).strip()
        lines.append(cur)
        s.mtext(lx, y + 118, lines, size=24, fill=MUTED)
        y += 210
    s.text(cx, cy + r + 50, '1 — основні, 2 — похідні, без позначки — третинні', size=22, fill=MUTED, anchor='middle')
    return s.save(L, 'd-kolorove-kolo')


def harmonies():
    s = SVG(1600, 860)
    s.title('Колірні гармонії', 'Чотири перевірені способи скласти палітру з кола')
    items = [
        ('Монохромна', 'Один колір: різна світлота', [8], ['#0d2f57', '#1F5FAE', '#7fa7d9', '#d6e3f4']),
        ('Комплементарна', 'Протилежні кольори: максимальний контраст', [2, 8], ['#FF7A00', '#ffe2c4', '#1F5FAE', '#0d2f57']),
        ('Аналогова', 'Сусідні кольори: спокійно й гармонійно', [0, 1, 2], ['#FFD400', '#FFA800', '#FF7A00', '#4a2c2a']),
        ('Тріадна', 'Три кольори через рівні проміжки: яскраво', [0, 4, 8], ['#FFD400', '#E2231A', '#1F5FAE', '#ffffff']),
    ]
    for k, (head, desc, marks, pal) in enumerate(items):
        x = 60 + k * 380
        wheel(s, x + 160, 340, 140, marks=marks)
        if len(marks) > 1:
            pts = []
            for i in marks:
                a = math.radians(i * 30)
                pts.append((x + 160 + 140 * 0.73 * math.sin(a), 340 - 140 * 0.73 * math.cos(a)))
            d = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in pts) + (' Z' if len(pts) > 2 else '')
            s.path(d, stroke=INK, sw=3, dash='8,6')
        s.text(x + 160, 540, head, size=30, weight=700, anchor='middle')
        a, b = desc.split(': ') if ': ' in desc else (desc, '')
        s.text(x + 160, 576, a + (':' if b else ''), size=20, fill=MUTED, anchor='middle')
        if b:
            s.text(x + 160, 602, b, size=20, fill=MUTED, anchor='middle')
        for j, c in enumerate(pal):
            s.rect(x + 20 + j * 72, 620, 64, 120, fill=c, rx=8, stroke=LINE if c == '#ffffff' else None, sw=2)
    s.text(800, 800, 'Кружечками позначено кольори, які беруть з кола; під колом приклад готової палітри', size=22,
           fill=MUTED, anchor='middle')
    return s.save(L, 'd-harmonii')


def psychology():
    s = SVG(1600, 900)
    s.title('Психологія кольору', 'Які асоціації викликає колір (для європейської культури)')
    items = [('#E2231A', 'Червоний', 'енергія, пристрасть, апетит, терміновість'),
             ('#FF7A00', 'Помаранчевий', 'дружність, тепло, бадьорість'),
             ('#FFD400', 'Жовтий', 'оптимізм, увага, радість'),
             ('#3AA935', 'Зелений', 'природа, здоров’я, екологія'),
             ('#1F5FAE', 'Синій', 'довіра, надійність, технології'),
             ('#6A2C91', 'Фіолетовий', 'креативність, мрія, розкіш'),
             ('#6b4226', 'Коричневий', 'затишок, натуральність, кава'),
             ('#1b1b1b', 'Чорний', 'елегантність, сила, преміум'),
             ('#f4f1ec', 'Білий / світлий', 'чистота, простір, легкість')]
    for i, (c, name, desc) in enumerate(items):
        col, row = i % 3, i // 3
        x, y = 60 + col * 505, 190 + row * 225
        s.rect(x, y, 470, 195, fill=SOFT, rx=18)
        s.rect(x + 22, y + 22, 150, 150, fill=c, rx=14, stroke=LINE if c == '#f4f1ec' else None)
        s.text(x + 196, y + 68, name, size=30, weight=700)
        words, lines, cur = desc.split(' '), [], ''
        for w in words:
            if len(cur + ' ' + w) > 20:
                lines.append(cur); cur = w
            else:
                cur = (cur + ' ' + w).strip()
        lines.append(cur)
        s.mtext(x + 196, y + 108, lines, size=22, fill=MUTED)
    return s.save(L, 'd-psykholohiia-koloru')


def rgb_cmyk():
    s = SVG(1600, 860)
    s.title('RGB і CMYK', 'Екран світить, папір поглинає')
    # RGB on black
    s.rect(60, 170, 700, 560, fill='#111111', rx=20)
    g = '<g style="isolation:isolate">'
    for (dx, dy, c) in ((0, -70, '#ff0000'), (-75, 55, '#00ff00'), (75, 55, '#0000ff')):
        g += f'<circle cx="{410 + dx}" cy="{440 + dy}" r="135" style="fill:{c};mix-blend-mode:screen"/>'
    s.add(g + '</g>')
    s.text(410, 225, 'RGB: адитивна модель', size=28, weight=700, fill='white', anchor='middle')
    s.text(410, 700, 'R + G + B = білий', size=24, fill='#dddddd', anchor='middle')
    # CMY on white
    s.rect(840, 170, 700, 560, fill='#ffffff', rx=20, stroke=LINE, sw=2)
    g = '<g style="isolation:isolate">'
    for (dx, dy, c) in ((0, -70, '#00aeef'), (-75, 55, '#ec008c'), (75, 55, '#fff200')):
        g += f'<circle cx="{1190 + dx}" cy="{440 + dy}" r="135" style="fill:{c};mix-blend-mode:multiply"/>'
    s.add(g + '</g>')
    s.text(1190, 225, 'CMYK: субтрактивна модель', size=28, weight=700, anchor='middle')
    s.text(1190, 700, 'C + M + Y ≈ темний, тому додають K (чорний)', size=22, fill=MUTED, anchor='middle')
    s.text(410, 790, 'Монітор, телефон, проєктор, веб', size=26, weight=600, anchor='middle')
    s.text(1190, 790, 'Друкарня: візитівки, плакати, листівки', size=26, weight=600, anchor='middle')
    return s.save(L, 'd-rgb-cmyk')


def hex_code():
    s = SVG(1600, 700)
    s.title('Як читати HEX-код кольору', 'Шістнадцяткове число: по 2 символи на кожен канал RGB')
    s.text(170, 340, '#', size=150, weight=700, family=HEAD, fill=MUTED)
    parts = [('E0', '#e61e3c', 'R = 224'), ('7A', GREEN, 'G = 122'), ('2F', BLUE, 'B = 47')]
    for i, (p, c, lbl) in enumerate(parts):
        x = 290 + i * 250
        s.text(x, 340, p, size=150, weight=700, family=HEAD, fill=c)
        s.path(f'M{x + 10},380 L{x + 10},400 L{x + 200},400 L{x + 200},380', stroke=c, sw=4)
        s.text(x + 105, 450, lbl, size=34, weight=700, fill=c, anchor='middle')
    s.rect(1120, 200, 380, 260, fill='#E07A2F', rx=20)
    s.text(1310, 500, 'rgb(224, 122, 47)', size=28, anchor='middle', weight=600)
    s.mtext(170, 560, ['00 = 0 (немає світла), FF = 255 (максимум).',
                       'Код #FFFFFF це білий, #000000 це чорний.'], size=26, fill=MUTED)
    return s.save(L, 'd-hex')


def rule_60_30_10():
    s = SVG(1600, 760)
    s.title('Правило 60–30–10', 'Як розподілити 3 кольори бренду на макеті')
    x, y, w, h = 80, 200, 860, 440
    s.rect(x, y, w, h, fill='#F3E9DC', rx=16)
    s.rect(x, y, w, 120, fill='#4A2C2A', rx=16)
    s.rect(x, y + 60, w, 60, fill='#4A2C2A')
    s.rect(x + 60, y + 170, 470, 210, fill='#4A2C2A', rx=12, opacity=0.9)
    s.rect(x + 590, y + 300, 210, 80, fill='#E07A2F', rx=40)
    s.text(x + 695, y + 350, 'Замовити', size=26, weight=700, fill='white', anchor='middle')
    s.text(x + 50, y + 75, 'КавоБус', size=40, weight=700, family=HEAD, fill='#F3E9DC')
    bars = [('#F3E9DC', '60 %', 'Основний (фон, великі площі)'), ('#4A2C2A', '30 %', 'Додатковий (заголовки, блоки)'),
            ('#E07A2F', '10 %', 'Акцент (кнопки, заклик до дії)')]
    yy = 220
    for c, p, desc in bars:
        s.rect(1010, yy, 100, 100, fill=c, rx=12, stroke=LINE)
        s.text(1135, yy + 45, p, size=40, weight=700, family=HEAD)
        s.text(1135, yy + 85, desc, size=22, fill=MUTED)
        yy += 140
    return s.save(L, 'd-60-30-10')


def font_classes():
    s = SVG(1600, 900)
    s.title('Класифікація шрифтів', 'Чотири групи, з якими працюватимемо')
    items = [('Антиква (із засічками)', 'Playfair Display', 'Playfair Display', 'класика, традиція, преміум'),
             ('Гротеск (без засічок)', 'Montserrat', 'Montserrat', 'сучасність, простота, технології'),
             ('Рукописні', 'Lobster', 'Lobster', 'тепло, дружність, ручна робота'),
             ('Акцидентні (декоративні)', 'Unbounded', 'Unbounded', 'характер, яскравість, тільки заголовки')]
    for i, (head, fam, name, mood) in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 60 + col * 760, 180 + row * 340
        s.rect(x, y, 720, 310, fill=SOFT, rx=18)
        s.text(x + 30, y + 52, head, size=26, weight=700, fill=MUTED)
        s.text(x + 30, y + 160, 'Кава й хліб', size=78, family=fam, weight=700 if fam in ('Montserrat', 'Unbounded') else 400)
        s.text(x + 30, y + 218, 'Ґґ Єє Іі Її 0123', size=34, family=fam)
        s.text(x + 30, y + 275, f'{name}: {mood}', size=22, fill=MUTED)
    return s.save(L, 'd-klasy-shryftiv')


def font_anatomy():
    s = SVG(1600, 820)
    s.title('Будова шрифту', 'Терміни, які трапляються в налаштуваннях програм')
    base, size = 560, 280
    x0 = 130
    s.text(x0, base, 'Шрифт', size=size, family='Playfair Display', weight=400)
    cap_h, x_h, asc, desc = base - 0.708 * size, base - 0.514 * size, base - 0.72 * size, base + 0.181 * size
    rows = [(asc, 'Висота виносного елемента (асцендер)', BLUE), (cap_h, 'Висота великої літери', GREEN),
            (x_h, 'Висота малої літери (x-висота)', ACCENT), (base, 'Базова лінія', RED), (desc, 'Нижній виносний елемент (десцендер)', '#6A2C91')]
    for y, lbl, c in rows:
        s.line(80, y, 1010, y, stroke=c, sw=3, dash='12,8')
    lab_y = [asc - 40, cap_h - 6, x_h + 8, base + 8, desc + 30]
    for (y, lbl, c), ly in zip(rows, lab_y):
        s.line(1010, y, 1030, ly, stroke=c, sw=2)
        s.text(1040, ly + 8, lbl, size=22, weight=600, fill=c)
    s.arrow(240, 700, 196, base + 4, stroke=INK, sw=3)
    s.text(250, 725, 'Засічка (serif)', size=24, weight=600)
    s.text(120, 790, 'Кегль (розмір шрифту) вимірюють у пунктах: 1 pt ≈ 0,353 мм', size=24, fill=MUTED)
    return s.save(L, 'd-anatomiia-shryftu')


def font_pairs():
    s = SVG(1600, 900)
    s.title('Пари шрифтів', 'Заголовковий шрифт + шрифт для тексту = контраст і гармонія')
    # subtitle size per pair: Unbounded is very wide and would overflow the card at 30 px
    pairs = [('Unbounded', 700, 24, 'Montserrat', 'Сучасна пара'),
             ('Playfair Display', 700, 30, 'Roboto', 'Класична пара'),
             ('Lobster', 400, 30, 'Rubik', 'Дружня пара')]
    for i, (h, hw, sub, b, lbl) in enumerate(pairs):
        x = 60 + i * 505
        s.rect(x, 180, 470, 560, fill=SOFT, rx=18)
        s.text(x + 30, 230, lbl, size=24, weight=700, fill=MUTED)
        s.text(x + 30, 340, 'Свіжа кава', size=54, family=h, weight=hw)
        s.text(x + 30, 395, 'щоранку біля коледжу', size=sub, family=h, weight=hw if h != 'Lobster' else 400)
        body = ['Готуємо каву з фургона щодня', 'з 7:30. Знижка 10 % для', 'студентів із квитком.']
        s.mtext(x + 30, 470, body, size=26, family=b)
        s.text(x + 30, 650, f'{h}', size=22, weight=700)
        s.text(x + 30, 685, f'+ {b}', size=22, weight=400, fill=MUTED)
    s.text(60, 820, 'Правила: не більше 2 шрифтів, контраст між ними, обов’язково підтримка української (Ґ, Є, І, Ї).',
           size=24, fill=MUTED)
    return s.save(L, 'd-pary-shryftiv')


if __name__ == '__main__':
    for f in (color_wheel, harmonies, psychology, rgb_cmyk, hex_code, rule_60_30_10, font_classes, font_anatomy, font_pairs):
        print(f())
