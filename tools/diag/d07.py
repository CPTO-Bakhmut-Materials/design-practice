"""Theory illustrations for lesson 07 (prepress: gamut, PDF/X boxes, imposition)."""
import os
from common import *

L = '07-prepres'
IMG = os.path.join(ROOT, 'lessons', L, 'img')
CREAM, BROWN, ORANGE = '#F3E9DC', '#4A2C2A', '#E07A2F'
CARD1 = os.path.join(ROOT, '.sandbox', 'prev', 'rv-1.png')


def gamut():
    s = SVG(1600, 860)
    s.title('Колірне охоплення: RGB і CMYK', 'Екран показує більше кольорів, ніж може надрукувати друкарська машина')
    cx, cy = 430, 500
    # RGB gamut: big triangle, CMYK: smaller hexagon inside
    s.path(f'M{cx},{cy - 290} L{cx + 300},{cy + 210} L{cx - 300},{cy + 210} Z', fill='#e8eefb', stroke=BLUE, sw=4)
    hexa = [(cx - 20, cy - 170), (cx + 150, cy - 10), (cx + 190, cy + 150), (cx - 10, cy + 175), (cx - 200, cy + 140),
            (cx - 150, cy - 30)]
    s.path('M' + ' L'.join(f'{x},{y}' for x, y in hexa) + ' Z', fill='#fdeee2', stroke=ORANGE, sw=4)
    s.text(cx, cy - 300, 'RGB (екран)', size=24, weight=700, fill=BLUE, anchor='middle')
    s.text(cx, cy + 60, 'CMYK', size=26, weight=700, fill=ORANGE, anchor='middle')
    s.text(cx, cy + 92, '(друк на крейдованому папері)', size=18, fill=MUTED, anchor='middle')
    for x, y in ((cx + 215, cy + 175), (cx - 30, cy - 225)):
        s.circle(x, y, 14, fill=GREEN)
    s.text(cx + 215, cy + 250, 'поза охопленням CMYK', size=18, fill=GREEN, weight=700, anchor='middle')
    # swatches
    x0 = 900
    rows = [('#00FF66', '#3DBE6E', 'Неоновий зелений'), ('#0050FF', '#2F5DB5', 'Яскраво-синій'),
            ('#FF00CC', '#D83C9E', 'Яскравий рожевий'), (ORANGE, '#DA7B3A', 'Kavobus Orange')]
    s.text(x0, 220, 'На екрані', size=22, weight=700)
    s.text(x0 + 200, 220, 'Приблизно на папері', size=22, weight=700)
    for i, (a, b, n) in enumerate(rows):
        y = 250 + i * 120
        s.rect(x0, y, 150, 90, fill=a, rx=8)
        s.rect(x0 + 200, y, 150, 90, fill=b, rx=8)
        s.text(x0 + 380, y + 52, n, size=20, fill=MUTED)
    s.mtext(70, 790, ['Кольори поза охопленням друкарня замінить найближчими, і вони стануть тьмянішими. Екранна кольоропроба',
                      '(soft proof) показує це заздалегідь — без пробного друку, паперу й фарби.'], size=22, fill=MUTED)
    return s.save(L, 'd-okhoplennia')


def boxes():
    s = SVG(1600, 880)
    s.title('Що всередині PDF для друкарні', 'Рамки сторінки й гарантії формату PDF/X')
    k = 1.6
    x0, y0 = 120, 190
    # media (with marks), bleed, trim
    mw, mh = 230 * k, 317 * k
    s.rect(x0, y0, mw, mh, fill='white', stroke=LINE, sw=2)
    bx, by = x0 + 7 * k, y0 + 7 * k
    s.rect(bx, by, 216 * k, 303 * k, fill=CREAM, stroke=RED, sw=3, dash='12,7')
    tx, ty = bx + 3 * k, by + 3 * k
    s.rect(tx, ty, 210 * k, 297 * k, stroke=INK, sw=3)
    for cx in (tx, tx + 210 * k):
        for cy in (ty, ty + 297 * k):
            dy = -1 if cy == ty else 1
            dx = -1 if cx == tx else 1
            s.line(cx, cy + dy * 6 * k, cx, cy + dy * 13 * k, sw=2)
            s.line(cx + dx * 6 * k, cy, cx + dx * 13 * k, cy, sw=2)
    s.text(x0 + mw / 2, y0 + mh + 40, 'poster-print.pdf', size=22, weight=700, anchor='middle')
    lx = 640
    rows = [(LINE, None, 'MediaBox', 'весь аркуш PDF разом із мітками обрізу'),
            (RED, '12,7', 'BleedBox', 'формат + виліт 3 мм: 216 × 303 мм'),
            (INK, None, 'TrimBox', 'формат після обрізу: 210 × 297 мм'),
            (INK, None, 'Мітки обрізу', 'короткі лінії точно на продовженні лінії обрізу')]
    y = 230
    for c, dash, h, d in rows:
        s.line(lx, y - 8, lx + 50, y - 8, stroke=c, sw=4, dash=dash)
        s.text(lx + 70, y, h, size=24, weight=700)
        s.text(lx + 70, y + 32, d, size=19, fill=MUTED)
        y += 85
    s.text(lx, y + 20, 'PDF/X гарантує:', size=26, weight=700, family=HEAD)
    s.mtext(lx, y + 64, ['✓ усі шрифти вбудовані у файл', '✓ вказано друкарський профіль (Output Intent), напр. ISO Coated v2',
                         '✓ немає того, що ламає друк: RGB без профілю, шифрування, відео',
                         '✓ рамки TrimBox і BleedBox записані — друкарня знає, де різати'],
            size=21, lh=1.55)
    return s.save(L, 'd-pdf-ramky')


def imposition():
    s = SVG(1600, 900)
    s.title('Розкладка (спуск полос)', 'Кілька виробів на одному аркуші з мітками обрізу')
    k = 1.75
    x0, y0 = 90, 190
    s.image(x0, y0, 210 * k, 297 * k, CARD1)
    s.rect(x0, y0, 210 * k, 297 * k, stroke=LINE, sw=2)
    s.text(x0 + 105 * k, y0 + 297 * k + 38, 'Візитівки: 10 шт. на A4', size=22, weight=700, anchor='middle')
    s.text(x0 + 105 * k, y0 + 297 * k + 68, '2 × 94 = 188 ≤ 210;  5 × 54 = 270 ≤ 297', size=18, fill=MUTED, anchor='middle')
    # A4 vs SRA4 for flyers
    x1 = 610
    k2 = 1.25
    s.text(x1, 215, 'Листівки A5 з вильотом: 154 × 216 мм', size=24, weight=700)
    ya = 250
    s.rect(x1, ya, 297 * k2, 210 * k2, fill='white', stroke=INK, sw=2)
    for i in range(2):
        s.rect(x1 + (i * 154 - 5.5) * k2, ya - 3 * k2, 154 * k2, 216 * k2, stroke=RED, sw=2, dash='8,5', fill=ORANGE,
               opacity=0.35)
    s.rect(x1, ya, 297 * k2, 210 * k2, stroke=INK, sw=3)
    s.text(x1 + 148 * k2, ya + 210 * k2 + 36, 'A4 297 × 210: 2 × 154 = 308 > 297 ✗', size=20, weight=700, fill=RED,
           anchor='middle')
    x2 = x1 + 297 * k2 + 60
    kk = k2
    s.rect(x2, ya, 320 * kk, 225 * kk, fill='white', stroke=INK, sw=2)
    for i in range(2):
        s.rect(x2 + (6 + i * 154) * kk, ya + 4.5 * kk, 154 * kk, 216 * kk, stroke=RED, sw=2, dash='6,4', fill=ORANGE,
               opacity=0.25)
    s.text(x2 + 160 * kk, ya + 225 * kk + 20, 'SRA4 320 × 225 ✓', size=20, weight=700, fill=GREEN, anchor='middle')
    s.mtext(x1, 640, ['A4 = рівно два A5 без вильотів, тож листівку з фоном «під обріз» на A4 по дві не розкласти.',
                      'Друкарні друкують на більших аркушах: SRA4 (320 × 225), SRA3 (320 × 450).',
                      'Зайве поле навколо — місце для вильотів і міток обрізу.'], size=20, fill=MUTED, lh=1.5)
    s.text(x1, 780, 'Готові шаблони: brand-day/templates/rozkladka-*.sla', size=20, weight=700)
    return s.save(L, 'd-rozkladka')


if __name__ == '__main__':
    for f in (gamut, boxes, imposition):
        print(f())
