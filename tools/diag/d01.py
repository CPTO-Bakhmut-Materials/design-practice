"""Illustrations for lesson 01 (intro, workflow, safety)."""
from common import *

L = '01-vstup'

def workflow():
    s = SVG(1600, 700)
    s.title('Маршрут дня', 'Від ідеї до файлів, готових для друкарні')
    steps = [('1', 'Бриф і мудборд', 'Inkscape'), ('2', 'Логотип', 'Inkscape'),
             ('3', 'Візитівка', 'Inkscape'), ('4', 'Ключовий візуал', 'Krita'),
             ('5', 'Плакат і листівка', 'Scribus'), ('6', 'Препрес', 'Scribus + Krita'),
             ('7', 'Пітч', 'мокапи')]
    colors = {'Inkscape': '#2f6fd6', 'Krita': '#6A2C91', 'Scribus': '#2e9e5b', 'Scribus + Krita': '#2e9e5b', 'мокапи': ACCENT}
    w = 196
    for i, (n, h, app) in enumerate(steps):
        x = 60 + i * (w + 22)
        c = colors[app]
        s.rect(x, 220, w, 260, fill=SOFT, rx=18)
        s.rect(x, 220, w, 12, fill=c, rx=4)
        s.circle(x + w / 2, 290, 34, fill=c)
        s.text(x + w / 2, 302, n, size=34, weight=700, fill='white', anchor='middle')
        words = h.split(' ')
        s.mtext(x + w / 2, 372, [words[0], ' '.join(words[1:])] if len(h) > 12 else [h], size=22, weight=700,
                anchor='middle')
        s.text(x + w / 2, 440, app, size=18, fill=c, weight=600, anchor='middle')
        if i < len(steps) - 1:
            s.arrow(x + w + 2, 350, x + w + 20, 350, stroke=MUTED, sw=3, head=10)
    s.mtext(60, 570, ['Усі програми безкоштовні та з відкритим кодом: Inkscape (вектор), Krita (растр), Scribus (верстка).',
                      'Вони працюють у Windows, macOS і Linux однаково — меню й інструменти ті самі.'], size=22, fill=MUTED)
    return s.save(L, 'd-marshrut-dnia')

def folders():
    s = SVG(1600, 820)
    s.title('Робоча тека', 'Одна тека на кожного здобувача: прізвище_НазваБренду')
    rows = [(0, 'Kovalenko_KavoBus/', 'ваша робоча тека'), (1, 'brief.pdf', 'бриф (урок 2)'), (1, 'moodboard.svg', 'мудборд (урок 2)'),
            (1, 'logo/', 'logo.svg, logo.pdf, logo.png, logo-mono.png (урок 3)'), (1, 'card/', 'card.svg, card-print.pdf (урок 4)'),
            (1, 'visual/', 'keyvisual.kra, keyvisual.png (урок 5)'), (1, 'poster/', 'poster.sla, poster-print.pdf (урок 6)'),
            (1, 'flyer/', 'flyer.sla, flyer-print.pdf (урок 6)'), (1, 'print/', 'розкладки, заявка до друкарні (урок 7)'),
            (1, 'mockups/', 'мокапи для презентації (урок 8)')]
    y = 200
    for lvl, name, note in rows:
        x = 90 + lvl * 60
        folder = name.endswith('/')
        if folder:
            s.path(f'M{x},{y - 22} h18 l6,6 h22 v26 h-46 Z', fill='#f2c14e')
        else:
            s.path(f'M{x + 6},{y - 24} h26 l8,8 v28 h-34 Z', fill='white', stroke=MUTED, sw=2)
        if lvl:
            s.line(90 + 22, y - 10, x - 8, y - 10, stroke=LINE, sw=2)
        s.text(x + 60, y, name, size=26, weight=700 if folder else 500)
        s.text(620, y, note, size=21, fill=MUTED)
        y += 56
    s.line(112, 200, 112, y - 66, stroke=LINE, sw=2)
    s.text(90, y + 20, 'Імена файлів — латиницею, без пробілів: так їх відкриє будь-яка програма й будь-яка ОС.', size=22,
           fill=MUTED)
    return s.save(L, 'd-robocha-teka')

def safety():
    s = SVG(1600, 820)
    s.title('Безпека та ергономіка за комп’ютером', 'Інструктаж з охорони праці перед початком роботи')
    items = [('Електробезпека', ['Не торкайтеся кабелів і розеток', 'мокрими руками', 'Помітили іскру, запах гару —', 'одразу кажіть викладачу']),
             ('Пожежна безпека', ['Знайте шлях евакуації', 'і місце вогнегасника', 'Не накривайте блок живлення', 'й монітор']),
             ('Постава', ['Спина спирається на спинку', 'Стопи на підлозі', 'Лікті під кутом 90°', 'Екран на рівні очей']),
             ('Очі', ['Відстань до екрана 50–70 см', 'Правило 20-20-20: кожні 20 хв', 'дивіться 20 с на 6 м', 'Кліпайте частіше'])]
    for i, (h, lines) in enumerate(items):
        x = 60 + (i % 2) * 750
        y = 190 + (i // 2) * 300
        s.rect(x, y, 720, 270, fill=SOFT, rx=18)
        s.circle(x + 60, y + 60, 32, fill=[RED, ACCENT, BLUE, GREEN][i])
        s.text(x + 60, y + 72, '!' if i < 2 else 'i', size=34, weight=700, fill='white', anchor='middle')
        s.text(x + 115, y + 72, h, size=30, weight=700)
        s.mtext(x + 115, y + 125, lines, size=22, fill=MUTED, lh=1.45)
    return s.save(L, 'd-bezpeka')

def ergonomics():
    s = SVG(1600, 760)
    s.title('Правильне робоче місце', 'Схема посадки за комп’ютером')
    P = 14  # one Minecraft "pixel"
    SKIN, SKIN_D, HAIR = '#c69079', '#a8705a', '#3b2513'
    SHIRT, SHIRT_D, PANTS, PANTS_D, SHOE = '#00a8a8', '#008c8c', '#3c3a9a', '#2e2c80', '#5a5a5a'

    def px(x, y, w, h, c):  # block in pixel units relative to (x, y)
        s.rect(x, y, w * P, h * P, fill=c)

    s.add('<g style="shape-rendering:crispEdges">')
    s.line(80, 700, 1520, 700, stroke=LINE, sw=3)
    # chair: backrest against the back, seat under the thighs
    s.rect(338, 330, 22, 222, fill=INK); s.rect(338, 532, 236, 20, fill=INK)
    s.rect(440, 552, 16, 148, fill=INK); s.rect(380, 690, 136, 10, fill=INK)
    # desk (front leg clears the knees) with keyboard
    s.rect(640, 460, 620, 20, fill='#b98b5e'); s.rect(700, 480, 16, 220, fill='#8a6340')
    s.rect(1220, 480, 16, 220, fill='#8a6340')
    s.rect(680, 448, 140, 12, fill='#555')
    # monitor facing the viewer's left, top edge at eye level
    s.rect(1040, 315, 28, 135, fill=INK); s.rect(1068, 360, 18, 92, fill='#555')
    s.rect(1036, 450, 90, 10, fill='#555'); s.rect(1040, 321, 6, 123, fill='#9cc9f0')
    # Steve, side view facing right
    hx, hy = 332, 252                      # head 8x8
    px(hx, hy, 8, 8, SKIN)
    px(hx, hy, 8, 2, HAIR); px(hx, hy, 3, 5, HAIR); px(hx + 3 * P, hy + 2 * P, 1, 1, HAIR)
    px(hx + 6 * P, hy + 4 * P, 1, 1, '#ffffff'); px(hx + 7 * P, hy + 4 * P, 1, 1, '#49408f')
    px(hx + 7 * P, hy + 5 * P, 1, 1, SKIN_D); px(hx + 6 * P, hy + 6 * P, 2, 1, '#6a4030')
    px(hx + 1 * P, hy + 7 * P, 1, 1, SKIN_D)
    px(360, 364, 4, 12, SHIRT); px(360, 364, 1, 12, SHIRT_D)            # torso
    s.rect(360, 476, 4 * P, 56, fill=PANTS)                                # hips
    s.rect(360, 482, 256, 50, fill=PANTS); s.rect(360, 522, 256, 10, fill=PANTS_D)   # thigh, horizontal
    s.rect(560, 532, 56, 154, fill=PANTS); s.rect(560, 532, 8, 154, fill=PANTS_D)    # shin, vertical
    s.rect(560, 672, 56, 28, fill=SHOE)                                    # shoe flat on the floor
    s.rect(374, 364, 56, 2 * P, fill=SHIRT)                                # sleeve
    s.rect(374, 392, 56, 68, fill=SKIN); s.rect(374, 392, 8, 68, fill=SKIN_D)        # upper arm, vertical
    s.rect(374, 418, 340, 42, fill=SKIN); s.rect(374, 452, 340, 8, fill=SKIN_D)      # forearm on the desk, hand on keys
    s.add('</g>')
    # angles
    s.path('M430,396 L452,396 L452,418', stroke=ACCENT, sw=3)   # elbow
    s.path('M538,532 L538,554 L560,554', stroke=ACCENT, sw=3)   # knee
    s.text(462, 404, '90°', size=26, weight=700, fill=ACCENT)
    s.text(478, 600, '90°', size=26, weight=700, fill=ACCENT)
    # eye line and distance
    s.line(444, 315, 1040, 315, stroke=RED, sw=3, dash='10,8')
    s.text(742, 300, 'верх екрана ≈ на рівні очей', size=22, fill=RED, weight=600, anchor='middle')
    s.dim(444, 215, 1040, 215, '50–70 см', size=22)
    s.mtext(130, 440, ['спина', 'на спинці'], size=20, lh=1.3, fill=MUTED)
    s.mtext(760, 530, ['лікті під 90°,', 'передпліччя на столі'], size=20, lh=1.3, fill=MUTED)
    s.text(588, 740, 'стопи повністю на підлозі', size=20, fill=MUTED, anchor='middle')
    return s.save(L, 'd-erhonomika')

if __name__ == '__main__':
    for f in (workflow, folders, safety, ergonomics):
        print(f())
