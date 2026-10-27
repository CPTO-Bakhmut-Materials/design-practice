"""Theory illustrations for lesson 06 (layout in Scribus: poster and flyer)."""
import os
from common import *

L = '06-verstka'
IMG = os.path.join(ROOT, 'lessons', L, 'img')
POSTER = os.path.join(IMG, 'result-poster.png')
FLY1 = os.path.join(IMG, 'result-flyer-1.png')
FLY2 = os.path.join(IMG, 'result-flyer-2.png')
KV = os.path.join(ROOT, 'brand-day', 'example', 'visual', 'keyvisual.png')
CREAM, BROWN, ORANGE = '#F3E9DC', '#4A2C2A', '#E07A2F'


def badge(s, x, y, n):
    s.circle(x, y, 17, fill=RED)
    s.text(x, y + 7, n, size=19, weight=700, fill='white', anchor='middle')


def grid():
    s = SVG(1600, 1080)
    s.title('Модульна сітка', 'Сторінку ділять на однакові модулі, а блоки ставлять точно по них')
    k = 2.6
    for i, (x0, show) in enumerate(((90, False), (720, True))):
        y0 = 190
        s.rect(x0, y0, 210 * k, 297 * k, fill='white', stroke=INK, sw=2)
        if show:
            s.image(x0, y0, 210 * k, 297 * k, POSTER)
            s.rect(x0, y0, 210 * k, 297 * k, fill='white', opacity=0.25)
        # 6 columns x 8 rows inside 10 mm margins, 4 mm gutters
        cw, rh, g = (190 - 5 * 4) / 6, (277 - 7 * 4) / 8, 4
        for c in range(6):
            for r in range(8):
                x = x0 + (10 + c * (cw + g)) * k
                y = y0 + (10 + r * (rh + g)) * k
                s.rect(x, y, cw * k, rh * k, fill=BLUE if not show else 'none', opacity=0.12 if not show else 1,
                       stroke=BLUE, sw=1.2, dash=None if not show else '5,4')
        if not show:
            s.rect(x0 + 10 * k, y0 + 10 * k, 190 * k, 277 * k, stroke=RED, sw=2)
            s.text(x0 + 105 * k, y0 + 297 * k + 40, 'Поля 10 мм, 6 колонок × 8 рядків', size=22, weight=700, anchor='middle')
            s.text(x0 + 105 * k, y0 + 297 * k + 72, 'проміжок між модулями 4 мм', size=19, fill=MUTED, anchor='middle')
        else:
            s.text(x0 + 105 * k, y0 + 297 * k + 40, 'Блоки плаката на сітці', size=22, weight=700, anchor='middle')
            s.text(x0 + 105 * k, y0 + 297 * k + 72, 'краї тексту й плашок збігаються', size=19, fill=MUTED, anchor='middle')
    lx = 1330
    s.mtext(lx, 260, ['Навіщо сітка', ''], size=24, weight=700)
    s.mtext(lx, 300, ['• однакові відступи', '• блоки вирівняні', '  між собою', '• макет виглядає', '  «зібраним»',
                      '• легко зробити', '  листівку в тому', '  самому стилі'], size=20, fill=MUTED)
    s.mtext(lx, 620, ['У Scribus сітку', 'будують напрямними:', 'Page → Manage', 'Guides'], size=20, fill=INK)
    return s.save(L, 'd-modulna-sitka')


def hierarchy():
    s = SVG(1600, 900)
    s.title('Типографічна ієрархія', 'Чотири рівні тексту: читач бачить їх саме в такому порядку')
    rows = [('1', 'Заголовок', 'Кава, що встигає з тобою', HEAD, 52, 700, BROWN, 'Unbounded Bold, 40 pt',
             'Головна думка. Найбільший, читається з 3–5 м'),
            ('2', 'Підзаголовок', 'Фургон «КавоБус» щоранку біля входу до коледжу', SANS, 26, 700, ORANGE,
             'Montserrat Bold, 16 pt', 'Пояснює заголовок: хто, де, коли'),
            ('3', 'Основний текст', 'Еспресо, лате, капучино — за 2 хвилини', SANS, 22, 400, INK,
             'Montserrat Regular, 12 pt', 'Подробиці: 3 короткі тези, не більше'),
            ('4', 'Заклик до дії', 'Перша кава — безкоштовно', SANS, 22, 700, 'white', 'Montserrat Bold, 14 pt',
             'Що зробити зараз. Виділяємо кольором (кнопка)')]
    y = 210
    for n, name, sample, fam, size, wt, col, spec, why in rows:
        badge(s, 85, y + 12, n)
        s.text(120, y + 4, name, size=24, weight=700)
        s.text(120, y + 36, spec, size=18, fill=MUTED)
        if n == '4':
            s.rect(500, y - 26, 420, 60, fill=ORANGE, rx=30)
            s.text(710, y + 12, sample, size=size, weight=wt, fill=col, family=fam, anchor='middle')
        else:
            s.text(500, y + 14, sample, size=size, weight=wt, fill=col, family=fam)
        s.text(1540, y + 60, why, size=19, fill=MUTED, anchor='end')
        s.line(60, y + 85, 1540, y + 85, stroke=LINE, sw=1)
        y += 150
    s.text(800, 860, 'Ієрархію створюють розмір, жирність, колір і відстань. Шрифтів — не більше двох.', size=24,
           weight=700, anchor='middle')
    return s.save(L, 'd-iierarkhiia')


def frames():
    s = SVG(1600, 860)
    s.title('Фрейми в Scribus', 'Будь-який вміст сторінки живе у фреймі: це «рамка-контейнер»')
    # image frame
    x0, y0 = 90, 200
    s.rect(x0, y0, 420, 300, fill=SOFT, stroke=INK, sw=2)
    s.line(x0, y0, x0 + 420, y0 + 300, stroke=MUTED, sw=1.5)
    s.line(x0 + 420, y0, x0, y0 + 300, stroke=MUTED, sw=1.5)
    s.text(x0 + 210, y0 + 345, 'Порожній фрейм зображення', size=22, weight=700, anchor='middle')
    s.text(x0 + 210, y0 + 377, 'хрестик = місце для картинки', size=19, fill=MUTED, anchor='middle')
    s.arrow(x0 + 450, y0 + 150, x0 + 560, y0 + 150, stroke=ACCENT, sw=4)
    s.text(x0 + 505, y0 + 130, 'Get Image', size=18, fill=ACCENT, weight=700, anchor='middle')
    x1 = 680
    s.image(x1, y0, 420, 300, KV)
    s.rect(x1, y0, 420, 300, stroke=RED, sw=3)
    s.text(x1 + 210, y0 + 345, 'Фрейм із зображенням', size=22, weight=700, anchor='middle')
    s.text(x1 + 210, y0 + 377, 'фото масштабується під фрейм', size=19, fill=MUTED, anchor='middle')
    # text frame
    x2 = 1170
    s.rect(x2, y0, 340, 300, fill='white', stroke=INK, sw=2)
    s.mtext(x2 + 20, y0 + 50, ['Еспресо, лате,', 'капучино — за 2', 'хвилини', 'Знижка 10 % для', 'студентів'],
            size=24, fill=INK)
    s.rect(x2 + 300, y0 + 280, 20, 20, fill='white', stroke=RED, sw=2)
    s.text(x2 + 310, y0 + 296, '+', size=20, weight=700, fill=RED, anchor='middle')
    s.text(x2 + 170, y0 + 345, 'Текстовий фрейм', size=22, weight=700, anchor='middle')
    s.text(x2 + 170, y0 + 377, 'червоний «+» = текст не вмістився', size=19, fill=RED, anchor='middle')
    s.mtext(90, 680, ['Фрейм можна переміщати й змінювати розмір, не чіпаючи вміст. Вміст (фото чи текст) редагують окремо:',
                      'F2 — властивості фрейму (Properties: положення, розмір, кольори),',
                      'F3 — властивості вмісту (Content Properties: шрифт і абзац для тексту, масштаб для фото).'],
            size=22, fill=MUTED)
    return s.save(L, 'd-frejmy')


def dpi_calc():
    s = SVG(1600, 760)
    s.title('Чи вистачить пікселів?', 'Ефективна роздільна здатність фото на макеті')
    rows = [('Ключовий візуал', '2551 × 3579 px'),
            ('Ширина фрейму на плакаті A4', '216 мм = 216 ÷ 25,4 = 8,5 дюйма'),
            ('Ефективна роздільна здатність', '2551 ÷ 8,5 = 300 dpi  ✓'),
            ('Те саме фото на плакаті A3 (303 мм)', '2551 ÷ 11,9 = 214 dpi  ✗')]
    y = 210
    for i, (a, b) in enumerate(rows):
        if i % 2 == 0:
            s.rect(60, y - 45, 1480, 90, fill=SOFT, rx=10)
        s.text(90, y + 8, a, size=24, fill=MUTED)
        col = GREEN if '✓' in b else RED if '✗' in b else INK
        s.text(800, y + 8, b, size=28, weight=700, fill=col)
        y += 110
    s.mtext(90, 680, ['Правило: для друку потрібно ≥ 300 dpi у реальному розмірі. Збільшуєте фото на макеті — dpi падає.'],
            size=22, fill=MUTED)
    return s.save(L, 'd-dpi')


def flyer_2up():
    s = SVG(1600, 820)
    s.title('Листівка A5: дві сторінки, дві на аркуші', 'Лицьовий і зворотний боки; на аркуші друку — дві листівки')
    k = 2.3
    y0 = 200
    s.image(90, y0, 148 * k, 210 * k, FLY1)
    s.rect(90, y0, 148 * k, 210 * k, stroke=LINE, sw=2)
    s.image(90 + 148 * k + 40, y0, 148 * k, 210 * k, FLY2)
    s.rect(90 + 148 * k + 40, y0, 148 * k, 210 * k, stroke=LINE, sw=2)
    s.text(90 + 148 * k / 2, y0 + 210 * k + 40, 'Сторінка 1 — лицьовий бік', size=20, weight=700, anchor='middle')
    s.text(90 + 148 * k * 1.5 + 40, y0 + 210 * k + 40, 'Сторінка 2 — зворотний бік', size=20, weight=700, anchor='middle')
    # A4 landscape with 2 A5
    k2 = 2.0
    x0, ya = 960, y0 + 40
    s.rect(x0, ya, 297 * k2, 210 * k2, fill='white', stroke=INK, sw=2)
    for i in range(2):
        x = x0 + (0.5 + i * 148) * k2
        s.image(x, ya, 148 * k2, 210 * k2, FLY1)
        s.rect(x, ya, 148 * k2, 210 * k2, stroke=RED, sw=1.5, dash='6,4')
    s.text(x0 + 297 * k2 / 2, ya + 210 * k2 + 40, 'A4 (297 × 210) = 2 × A5 (148 × 210) після обрізу', size=20, weight=700,
           anchor='middle')
    s.mtext(x0, ya + 210 * k2 + 90, ['З вильотами дві листівки займають 308 × 216 мм,', 'тому для друку беруть аркуш SRA4 (урок 7).'],
            size=19, fill=MUTED)
    return s.save(L, 'd-lystivka-a5')


if __name__ == '__main__':
    for f in (grid, hierarchy, frames, dpi_calc, flyer_2up):
        print(f())
