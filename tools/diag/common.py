"""Tiny SVG builder for theory illustrations; renders PNG via Inkscape CLI (brand-day fonts)."""
import os, subprocess, sys, html

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import cap

ROOT = cap.ROOT
INK = '#2b2522'      # text
MUTED = '#7a7068'
LINE = '#cfc7bd'
BG = '#ffffff'
SOFT = '#f6f3ef'
ACCENT = '#e07a2f'   # orange
RED = '#e61e3c'
GREEN = '#2e9e5b'
BLUE = '#2f6fd6'
SANS = 'Montserrat'
HEAD = 'Unbounded'


def esc(s):
    return html.escape(str(s), quote=False)


class SVG:
    def __init__(self, w, h, bg=BG):
        self.w, self.h = w, h
        self.items = []
        self.defs = []
        if bg:
            self.rect(0, 0, w, h, fill=bg)

    def add(self, s):
        self.items.append(s)
        return self

    def rect(self, x, y, w, h, fill='none', stroke=None, sw=2, rx=0, dash=None, opacity=1):
        st = f'fill:{fill};opacity:{opacity};'
        if stroke:
            st += f'stroke:{stroke};stroke-width:{sw};'
            if dash:
                st += f'stroke-dasharray:{dash};'
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="{st}"/>')

    def circle(self, cx, cy, r, fill='none', stroke=None, sw=2, opacity=1, dash=None):
        st = f'fill:{fill};opacity:{opacity};'
        if stroke:
            st += f'stroke:{stroke};stroke-width:{sw};'
            if dash:
                st += f'stroke-dasharray:{dash};'
        return self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" style="{st}"/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=2, dash=None, cap='round'):
        st = f'stroke:{stroke};stroke-width:{sw};stroke-linecap:{cap};fill:none;'
        if dash:
            st += f'stroke-dasharray:{dash};'
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="{st}"/>')

    def path(self, d, fill='none', stroke=None, sw=2, dash=None, opacity=1, extra=''):
        st = f'fill:{fill};opacity:{opacity};'
        if stroke:
            st += f'stroke:{stroke};stroke-width:{sw};stroke-linejoin:round;stroke-linecap:round;'
            if dash:
                st += f'stroke-dasharray:{dash};'
        return self.add(f'<path d="{d}" style="{st}{extra}"/>')

    def text(self, x, y, s, size=28, weight=400, fill=INK, anchor='start', family=SANS, style='', ls=None):
        st = f'font-family:{family};font-size:{size}px;font-weight:{weight};fill:{fill};text-anchor:{anchor};{style}'
        if ls is not None:
            st += f'letter-spacing:{ls}px;'
        return self.add(f'<text x="{x}" y="{y}" style="{st}">{esc(s)}</text>')

    def mtext(self, x, y, lines, size=26, lh=1.35, **kw):
        for i, s in enumerate(lines):
            self.text(x, y + i * size * lh, s, size=size, **kw)
        return self

    def arrow(self, x1, y1, x2, y2, stroke=INK, sw=3, head=14):
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * 0.8 * math.cos(a), y2 - head * 0.8 * math.sin(a)
        self.line(x1, y1, bx, by, stroke=stroke, sw=sw)
        p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
        p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
        return self.path(f'M{x2},{y2} L{p1[0]},{p1[1]} L{p2[0]},{p2[1]} Z', fill=stroke)

    def dim(self, x1, y1, x2, y2, label, stroke=INK, size=22, off=0, side='above'):
        """Dimension line with arrows at both ends and a label."""
        self.arrow((x1 + x2) / 2, (y1 + y2) / 2, x1, y1, stroke=stroke, sw=2, head=12)
        self.arrow((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, stroke=stroke, sw=2, head=12)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if y1 == y2:
            self.text(mx, my - 10 if side == 'above' else my + size + 6, label, size=size, anchor='middle', fill=stroke, weight=600)
        else:
            self.text(mx + 12, my + size / 3, label, size=size, anchor='start', fill=stroke, weight=600)
        return self

    def title(self, s, sub=None, x=60, y=80):
        self.text(x, y, s, size=40, weight=700, family=HEAD)
        if sub:
            self.text(x, y + 46, sub, size=24, fill=MUTED)
        return self

    def image(self, x, y, w, h, href, preserve='xMidYMid slice'):
        return self.add(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{preserve}" xlink:href="{href}"/>')

    def svg(self):
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">{defs}{"".join(self.items)}</svg>')

    def save(self, lesson, name, scale=1):
        d = os.path.join(ROOT, 'lessons', lesson, 'img')
        os.makedirs(d, exist_ok=True)
        src = os.path.join(ROOT, '.sandbox', 'diag', lesson + '__' + name + '.svg')
        os.makedirs(os.path.dirname(src), exist_ok=True)
        open(src, 'w', encoding='utf-8').write(self.svg())
        out = os.path.join(d, name + '.png')
        cap.run('inkscape', src, '--export-type=png', f'--export-width={int(self.w * scale)}',
                f'--export-filename={out}')
        return out
