"""Theory illustrations for lesson 08 (mockups, pitch, price)."""
import os
from common import *

L = '08-pitch'
CREAM, BROWN, ORANGE = '#F3E9DC', '#4A2C2A', '#E07A2F'
IMG = os.path.join(ROOT, 'lessons', L, 'img')


def mockup_idea():
    s = SVG(1600, 760)
    s.title('Що таке мокап', 'Ваш плоский дизайн, вставлений у реальну сцену')
    s.image(140, 200, 330, 330 * 842 / 595, os.path.join(ROOT, '.sandbox', 'home', 'Kovalenko_KavoBus', 'mockups',
                                                               'plakat-page001.png'), preserve='xMidYMid meet')
    s.text(305, 700, 'Плоский макет', size=22, weight=700, anchor='middle')
    s.arrow(530, 420, 640, 420, stroke=ACCENT, sw=5)
    s.image(670, 200, 860, 860 * 1678 / 2970, os.path.join(IMG, 'result-mockup-stina.jpg'))
    s.text(1100, 720, 'Мокап: клієнт одразу бачить, як це виглядатиме «в житті»', size=22, weight=700, anchor='middle')
    return s.save(L, 'd-mokap')


def pitch():
    s = SVG(1600, 700)
    s.title('Пітч за 90 секунд', 'Чотири частини — і жодної зайвої')
    parts = [(20, 'Бренд', ['Назва, для кого,', '3 прикметники'], CREAM),
             (30, 'Рішення', ['Чому такий логотип,', 'кольори, шрифт.', 'На екрані — мокапи'], ORANGE),
             (25, 'Ціна', ['Робота + друк =', 'сума для клієнта'], CREAM),
             (15, 'Фінал', ['3 терміни англійською,', '«Дякую!»'], BROWN)]
    x, k = 80, 1440 / 90
    for sec, name, lines, col in parts:
        w = sec * k
        fg = 'white' if col in (ORANGE, BROWN) else INK
        s.rect(x, 200, w - 8, 120, fill=col, rx=12)
        s.text(x + 20, 252, name, size=30, weight=700, fill=fg, family=HEAD)
        s.text(x + 20, 296, f'{sec} с', size=24, fill=fg)
        s.mtext(x + 4, 380, lines, size=21, fill=MUTED)
        x += w
    s.line(80, 520, 1520, 520, stroke=LINE, sw=2)
    for t in range(0, 91, 15):
        xx = 80 + t * k
        s.line(xx, 512, xx, 528, stroke=MUTED, sw=2)
        s.text(xx, 556, f'{t} с', size=18, fill=MUTED, anchor='middle')
    s.mtext(80, 630, ['Говоріть про клієнта й рішення, а не про програми. Не «я намалювала в Inkscape», а «помаранчевий — колір ранку й енергії».'],
            size=21, fill=MUTED)
    return s.save(L, 'd-pitch')


def price():
    s = SVG(1600, 820)
    s.title('Скільки коштує фірмовий стиль', 'Ціна для клієнта = робота дизайнера + друк')
    rows = [('Бриф і мудборд', '0,5'), ('Логотип', '1'), ('Візитівка', '0,75'), ('Ключовий візуал', '0,75'),
            ('Плакат і листівка', '0,8'), ('Препрес і заявка', '0,4')]
    y = 210
    s.text(90, y, 'Робота', size=24, weight=700)
    s.text(560, y, 'годин', size=24, weight=700, anchor='end')
    for i, (a, b) in enumerate(rows):
        yy = y + 50 + i * 46
        if i % 2 == 0:
            s.rect(70, yy - 32, 510, 46, fill=SOFT, rx=8)
        s.text(90, yy, a, size=22)
        s.text(560, yy, b, size=22, weight=700, anchor='end')
    s.text(90, y + 50 + 6 * 46 + 10, 'Разом', size=24, weight=700)
    s.text(560, y + 50 + 6 * 46 + 10, '4,2', size=24, weight=700, anchor='end')
    x = 700
    lines = [('Робота', '4,2 год × 200 грн/год', '= 840 грн'), ('Друк (із заявки)', 'візитівки, плакати, листівки', '= 1100 грн'),
             ('Ціна для клієнта', '', '≈ 1940 грн')]
    yy = 260
    for i, (a, b, c) in enumerate(lines):
        last = i == len(lines) - 1
        if last:
            s.rect(x - 20, yy - 50, 840, 100, fill=ORANGE, rx=14)
        fg = 'white' if last else INK
        s.text(x, yy, a, size=26, weight=700, fill=fg)
        if b:
            s.text(x, yy + 34, b, size=20, fill=MUTED)
        s.text(x + 800, yy + (10 if last else 0), c, size=34 if last else 28, weight=700, fill=fg, anchor='end',
               family=HEAD if last else SANS)
        yy += 140
    s.mtext(70, 740, ['Ставка 200 грн/год і ціни друку — умовні, для вправи. Реальні ставки дизайнерів і ціни друкарень дізнайтеся самі:',
                      'відкрийте сайт 2–3 друкарень свого міста й порівняйте.'], size=20, fill=MUTED)
    return s.save(L, 'd-tsina')


if __name__ == '__main__':
    for f in (mockup_idea, pitch, price):
        print(f())
