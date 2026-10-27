"""Theory illustrations for lesson 05 (raster, resolution, layers)."""
import os
from common import *

L = '05-kliuchovyi-vizual'
PH = os.path.join(ROOT, 'brand-day', 'photos', '01-kavobus')


def resolution():
    s = SVG(1600, 860)
    s.title('Роздільна здатність', 'Скільки пікселів потрібно для друку')
    s.mtext(60, 200, ['dpi (ppi) — кількість пікселів на 1 дюйм (25,4 мм) відбитка.',
                      'Розмір у пікселях = розмір у мм ÷ 25,4 × dpi'], size=26)
    rows = [('Екран, соцмережі', '72–96 dpi', 'достатньо: пікселі менші за піксель екрана'),
            ('Друк (плакат, візитівка)', '300 dpi', 'стандарт друкарень'),
            ('Великий банер (дивляться здалеку)', '100–150 dpi', 'з відстані 3 м пікселів не видно')]
    y = 330
    for a, b, c in rows:
        s.rect(60, y - 44, 1480, 74, fill=SOFT, rx=10)
        s.text(90, y, a, size=26, weight=700)
        s.text(720, y, b, size=28, weight=700, fill=ACCENT)
        s.text(960, y, c, size=21, fill=MUTED)
        y += 90
    s.text(60, 640, 'Приклад: плакат A4 з вильотами 3 мм = 216 × 303 мм', size=26, weight=700)
    s.text(60, 695, '216 ÷ 25,4 × 300 = 2551 px  ·  303 ÷ 25,4 × 300 = 3579 px', size=30, weight=700, fill=BLUE, family=HEAD)
    s.text(60, 760, 'Фото 1000 px завширшки на плакаті A4 матиме лише ≈ 120 dpi — буде розмитим.', size=24, fill=MUTED)
    return s.save(L, 'd-rozdilna-zdatnist')


def layers():
    s = SVG(1600, 860)
    s.title('Шари', 'Макет складається з прозорих «плівок» одна над одною')
    names = [('Зерна (вирізані)', ACCENT, 'kavovi-zerna-na-bilomu.jpg'), ('Затемнення (Levels)', '#333333', None),
             ('Текстура зерен', '#6b4226', 'zerna-tekstura.jpg'), ('Background (білий)', '#ffffff', None)]
    for i, (n, c, img) in reversed(list(enumerate(names))):
        y = 230 + i * 120
        x = 120 + i * 40
        s.add(f'<g transform="translate({x},{y}) skewX(-30) scale(1,0.5)">'
              f'<rect x="0" y="0" width="520" height="420" style="fill:{c};fill-opacity:{0.85 if img is None else 0.95};stroke:{INK};stroke-width:3"/></g>')
        s.text(x + 640, y + 110, n, size=26, weight=700)
        s.line(x + 470, y + 100, x + 620, y + 100, stroke=MUTED, sw=2, dash='6,6')
    s.mtext(1180, 260, ['Верхні шари закривають нижні.', 'Прозорі ділянки показують', 'те, що під ними.',
                        '', 'Шари фільтрів (Filter Layer)', 'змінюють усе, що нижче,', 'не псуючи оригінал.'], size=24, fill=MUTED)
    return s.save(L, 'd-shary')


def selections():
    s = SVG(1600, 760)
    s.title('Інструменти виділення', 'Виділення — це «трафарет»: зміни діють лише всередині нього')
    rows = [('Прямокутне / еліптичне', 'Ctrl+R / J', 'проста геометрична область'),
            ('Ласо (Freehand)', '—', 'обвести мишею вручну'),
            ('Суміжна область (Contiguous, «чарівна паличка»)', 'Ctrl+?', 'клацання по однорідному фону: білий, небо'),
            ('Подібний колір (Similar Color)', '—', 'усі пікселі схожого кольору по всьому шару'),
            ('Безьє / магнітне виділення', '—', 'точний контур складного об’єкта')]
    y = 200
    for a, b, c in rows:
        s.rect(60, y - 42, 1480, 72, fill=SOFT, rx=10)
        s.text(90, y, a, size=24, weight=700)
        s.text(980, y, c, size=21, fill=MUTED)
        y += 88
    s.mtext(60, 680, ['Shift + клацання — додати до виділення, Alt + клацання — відняти. Ctrl+Shift+A — зняти виділення.'],
            size=22, fill=MUTED)
    return s.save(L, 'd-vydilennia')


if __name__ == '__main__':
    for f in (resolution, layers, selections):
        print(f())
