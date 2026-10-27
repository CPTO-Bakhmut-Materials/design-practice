"""Scribus script: imposition templates (step and repeat with crop marks).

Run:  scribus -g -ns -py tools/build_imposition.py <workdir>
<workdir>/print/ receives rozkladka-vizytivky.sla (10 cards on A4) and rozkladka-lystivky.sla
(2 A5 flyers on SRA4). Frames link ../card/card-print.pdf and ../flyer/flyer-print.pdf by relative
path, so a copy of the template in any student's print/ folder shows that student's work.
Page 2 of each template shows page 2 (back side) of the source PDF: the scripter API cannot pick a
PDF page, so back_sides() sets Pagenumber (and colour management) in the saved file.
"""
import os, re, sys
import scribus as S

W = sys.argv[1]
MARK, GAP = 5, 2  # crop mark length and distance from the bleed edge, mm


def marks(xs, ys, x0, y0, x1, y1):
    """Crop marks in the margins around the block (x0,y0)-(x1,y1) at trim lines xs, ys."""
    for x in xs:
        for a, b in ((y0 - GAP - MARK, y0 - GAP), (y1 + GAP, y1 + GAP + MARK)):
            l = S.createLine(x, a, x, b)
            S.setLineColor('Registration', l); S.setLineWidth(0.25, l)
    for y in ys:
        for a, b in ((x0 - GAP - MARK, x0 - GAP), (x1 + GAP, x1 + GAP + MARK)):
            l = S.createLine(a, y, b, y)
            S.setLineColor('Registration', l); S.setLineWidth(0.25, l)


def grid(pdf, cols, rows, w, h, bleed, sheet):
    sw, sh = sheet
    ox, oy = (sw - cols * w) / 2, (sh - rows * h) / 2
    for page in (1, 2):
        S.gotoPage(page)
        for j in range(rows):
            for i in range(cols):
                f = S.createImage(ox + i * w, oy + j * h, w, h, f'p{page}-{j + 1}-{i + 1}')
                S.loadImage(pdf, f)
                S.setScaleImageToFrame(False, True, f)  # 100 %: PDF pages are rounded up to whole pt
        xs = [ox + i * w + d for i in range(cols) for d in (bleed, w - bleed)]
        ys = [oy + j * h + d for j in range(rows) for d in (bleed, h - bleed)]
        marks(xs, ys, ox, oy, ox + cols * w, oy + rows * h)


def back_sides(sla):
    """Back pages show PDF page 2; colour management on, so PDF/X is available in the export dialog."""
    s = open(sla, encoding='utf-8').read()
    for a in ('DPuse', 'DPSo', 'HCMS'):
        s = s.replace(f'{a}="0"', f'{a}="1"', 1)
    s = re.sub(r'<PAGEOBJECT [^>]*ANNAME="p2-[^>]*', lambda m: m.group(0).replace('Pagenumber="0"', 'Pagenumber="2"'), s)
    open(sla, 'w', encoding='utf-8').write(s)


def cards():
    S.newDocument((210, 297), (0, 0, 0, 0), S.PORTRAIT, 1, S.UNIT_MILLIMETERS, S.PAGE_1, 0, 2)
    grid(os.path.join(W, 'card', 'card-print.pdf'), 2, 5, 94, 54, 2, (210, 297))
    S.saveDocAs(os.path.join(W, 'print', 'rozkladka-vizytivky.sla'))
    S.closeDoc()
    back_sides(os.path.join(W, 'print', 'rozkladka-vizytivky.sla'))


def flyers():
    S.newDocument((320, 225), (0, 0, 0, 0), S.PORTRAIT, 1, S.UNIT_MILLIMETERS, S.PAGE_1, 0, 2)
    grid(os.path.join(W, 'flyer', 'flyer-print.pdf'), 2, 1, 154, 216, 3, (320, 225))
    S.saveDocAs(os.path.join(W, 'print', 'rozkladka-lystivky.sla'))
    S.closeDoc()
    back_sides(os.path.join(W, 'print', 'rozkladka-lystivky.sla'))


cards()
flyers()
