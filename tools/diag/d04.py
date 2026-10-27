"""Theory illustrations for lesson 04 (business card, print basics)."""
import os
from common import *

L = '04-vizytivka'
LOGO = os.path.join(ROOT, 'brand-day', 'example', 'logo', 'logo.png')
CREAM, BROWN, ORANGE = '#F3E9DC', '#4A2C2A', '#E07A2F'


def bleed_safe():
    s = SVG(1600, 900)
    s.title('Обріз, виліт і безпечна зона', 'Три рамки, які має кожен макет для друку')
    k = 9  # px per mm
    x0, y0 = 160, 200
    # bleed area
    s.rect(x0, y0, 94 * k, 54 * k, fill=CREAM)
    s.rect(x0, y0, 94 * k, 54 * k, stroke=RED, sw=3, dash='14,8')
    # trim
    s.rect(x0 + 2 * k, y0 + 2 * k, 90 * k, 50 * k, stroke=INK, sw=3)
    # safe
    s.rect(x0 + 6 * k, y0 + 6 * k, 82 * k, 42 * k, stroke=BLUE, sw=3, dash='6,6')
    s.image(x0 + 22 * k, y0 + 13 * k, 50 * k, 26 * k, LOGO, preserve='xMidYMid meet')
    # crop marks
    for cx in (x0 + 2 * k, x0 + 92 * k):
        for cy in (y0 + 2 * k, y0 + 52 * k):
            s.line(cx, cy - (60 if cy < y0 + 10 * k else -60), cx, cy - (25 if cy < y0 + 10 * k else -25), sw=2)
            s.line(cx - (60 if cx < x0 + 10 * k else -60), cy, cx - (25 if cx < x0 + 10 * k else -25), cy, sw=2)
    # dims
    s.dim(x0 + 2 * k, y0 + 54 * k + 50, x0 + 92 * k, y0 + 54 * k + 50, '90 мм (формат після обрізу)', size=22)
    s.dim(x0 - 60, y0 + 2 * k, x0 - 60, y0 + 52 * k, '50', size=22)
    lx = 1070
    rows = [(RED, '14,8', 'Виліт (bleed), +2 мм', 'Фон і фото заходять за край, щоб після обрізу не лишилося білої смужки.'),
            (INK, None, 'Лінія обрізу (trim)', 'Справжній розмір виробу: 90 × 50 мм.'),
            (BLUE, '6,6', 'Безпечна зона, −4 мм', 'Увесь текст і логотип — тільки всередині, бо різак може зсунутися на 1–2 мм.'),
            (INK, None, 'Мітки обрізу', 'Короткі лінії поза макетом: по них друкарня ріже аркуш.')]
    y = 230
    for c, dash, h, d in rows:
        s.line(lx, y, lx + 50, y, stroke=c, sw=4, dash=dash)
        s.text(lx + 70, y + 8, h, size=24, weight=700)
        words, lines, cur = d.split(' '), [], ''
        for w in words:
            if len(cur + ' ' + w) > 34:
                lines.append(cur); cur = w
            else:
                cur = (cur + ' ' + w).strip()
        lines.append(cur)
        s.mtext(lx + 70, y + 42, lines, size=19, fill=MUTED)
        y += 60 + 26 * len(lines) + 20
    s.text(800, 860, 'Документ із вильотами: 90 + 2 + 2 = 94 мм × 50 + 2 + 2 = 54 мм', size=26, weight=700, anchor='middle')
    return s.save(L, 'd-vylit-bezpechna-zona')


def card_sizes():
    s = SVG(1600, 760)
    s.title('Формати візитівок', 'Найпоширеніші розміри (мм)')
    k = 3.9
    items = [('Європейський', 85, 55, 'ЄС, Україна'), ('Стандарт СНД', 90, 50, 'наш шаблон'), ('США', 88.9, 50.8, '3,5 × 2 дюйми'),
             ('Квадратний', 55, 55, 'для креативних брендів')]
    x = 70
    for name, w, h, note in items:
        s.rect(x, 230, w * k, h * k, fill=CREAM if name != 'Стандарт СНД' else ORANGE, rx=6, stroke=LINE)
        s.text(x + w * k / 2, 230 + h * k / 2 + 10, f'{w:g} × {h:g}', size=26, weight=700, anchor='middle',
               fill='white' if name == 'Стандарт СНД' else INK)
        s.text(x, 230 + 55 * k + 50, name, size=24, weight=700)
        s.text(x, 230 + 55 * k + 82, note, size=19, fill=MUTED)
        x += 390
    s.mtext(70, 690, ['Папір: 300–350 г/м² (крейдований або дизайнерський). Кольоровість: 4+4 (обидва боки кольорові) чи 4+0.'],
            size=22, fill=MUTED)
    return s.save(L, 'd-formaty-vizytivok')


def card_content():
    s = SVG(1600, 820)
    s.title('Що розмістити на візитівці', 'Ієрархія: від найважливішого до другорядного')
    k = 7.5
    # front
    x0, y0 = 80, 200
    s.rect(x0, y0, 90 * k, 50 * k, fill=CREAM, rx=6)
    s.image(x0 + 17 * k, y0 + 10 * k, 56 * k, 30 * k, LOGO, preserve='xMidYMid meet')
    s.text(x0 + 45 * k, y0 + 50 * k + 50, 'Лицьовий бік: логотип (+ слоган)', size=24, weight=700, anchor='middle')
    # back
    x1 = 860
    s.rect(x1, y0, 90 * k, 50 * k, fill=BROWN, rx=6)
    s.text(x1 + 6 * k, y0 + 15 * k, 'Олена Коваленко', size=34, weight=700, fill=CREAM)
    s.text(x1 + 6 * k, y0 + 21 * k, 'засновниця і бариста', size=22, fill=ORANGE)
    s.mtext(x1 + 6 * k, y0 + 33 * k, ['+380 67 000 00 00', '@kavobus', 'Біля входу до коледжу, з 7:30'], size=19,
            fill=CREAM, lh=1.4)
    s.image(x1 + 64 * k, y0 + 24 * k, 20 * k, 20 * k, os.path.join(ROOT, '.sandbox', 'diag', 'qr.png'), preserve='none')
    s.text(x1 + 45 * k, y0 + 50 * k + 50, 'Зворотний бік: людина й контакти', size=24, weight=700, anchor='middle')
    nums = [(x1 + 4 * k, y0 + 11 * k, '1'), (x1 + 4 * k, y0 + 19 * k, '2'), (x1 + 4 * k, y0 + 30 * k, '3'), (x1 + 62 * k, y0 + 22 * k, '4')]
    for x, y, n in nums:
        s.circle(x - 10, y, 16, fill=RED)
        s.text(x - 10, y + 7, n, size=18, weight=700, fill='white', anchor='middle')
    s.mtext(80, 700, ['1 — ім’я (найбільший текст), 2 — посада (акцентний колір), 3 — контакти (дрібніше, але не менше 7 pt),',
                      '4 — QR-код (не менше 15 × 15 мм, темний на світлому, з білою рамкою навколо).'], size=22, fill=MUTED)
    return s.save(L, 'd-zmist-vizytivky')


def min_sizes():
    s = SVG(1600, 700)
    s.title('Мінімальні розміри для друку', 'Що буде нечитабельним на папері')
    rows = [('Текст', '≥ 7 pt', 'дрібніше розпливається'), ('Тонка лінія', '≥ 0,25 pt (0,1 мм)', 'тонші не віддрукуються'),
            ('QR-код', '≥ 15 × 15 мм', 'інакше телефон не прочитає'), ('Виліт', '2 мм', '3 мм для плакатів, 5 мм для книжок'),
            ('Відступ від краю', '≥ 3–4 мм', 'безпечна зона'), ('Растрові фото', '300 dpi', 'у реальному розмірі на макеті')]
    for i, (a, b, c) in enumerate(rows):
        y = 190 + i * 80
        if i % 2 == 0:
            s.rect(60, y - 45, 1480, 76, fill=SOFT, rx=10)
        s.text(90, y, a, size=26, weight=700)
        s.text(560, y, b, size=26, weight=700, fill=ORANGE)
        s.text(980, y, c, size=22, fill=MUTED)
    return s.save(L, 'd-minimalni-rozmiry')


def imposition_calc():
    s = SVG(1600, 900)
    s.title('Скільки візитівок уміщується на A4', 'Розрахунок розкладки')
    k = 2.25
    x0, y0 = 90, 170
    s.rect(x0, y0, 210 * k, 297 * k, fill='white', stroke=INK, sw=2)
    ox, oy = (210 - 2 * 94) / 2, (297 - 5 * 54) / 2
    for i in range(2):
        for j in range(5):
            x = x0 + (ox + i * 94) * k
            y = y0 + (oy + j * 54) * k
            s.rect(x, y, 94 * k, 54 * k, fill=CREAM, stroke=RED, sw=1.5, dash='6,4')
            s.rect(x + 2 * k, y + 2 * k, 90 * k, 50 * k, stroke=INK, sw=1.5)
    s.text(x0 + 105 * k, y0 + 297 * k + 40, 'A4: 210 × 297 мм', size=22, weight=700, anchor='middle')
    lx = 760
    lines = [('Розмір однієї візитівки з вильотами', '94 × 54 мм'),
             ('По ширині A4', '210 ÷ 94 = 2,2 → 2 шт.'),
             ('По висоті A4', '297 ÷ 54 = 5,5 → 5 шт.'),
             ('Разом на аркуші', '2 × 5 = 10 шт.'),
             ('Тираж 100 шт.', '100 ÷ 10 = 10 аркушів')]
    y = 240
    for a, b in lines:
        s.text(lx, y, a, size=22, fill=MUTED)
        s.text(lx, y + 40, b, size=32, weight=700)
        y += 110
    s.text(lx, y + 20, 'Якщо повернути візитівку вертикально: 210 ÷ 54 = 3, 297 ÷ 94 = 3 → лише 9 шт.', size=19, fill=MUTED)
    return s.save(L, 'd-rozkladka-a4')


if __name__ == '__main__':
    for f in (bleed_safe, card_sizes, card_content, min_sizes, imposition_calc):
        print(f())
