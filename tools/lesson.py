"""Helpers for lesson capture scripts: snap() = screenshot of the app window + annotations.

Marks/crops are given in absolute screen coordinates; they are converted to window
coordinates automatically.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cap
from annotate import annotate

ROOT = cap.ROOT
RAW = os.path.join(ROOT, '.sandbox', 'raw')


class Session:
    def __init__(self, lesson_dir, app_cls):
        self.dir = os.path.join(ROOT, 'lessons', lesson_dir, 'img')
        self.cls = app_cls
        os.makedirs(self.dir, exist_ok=True)
        os.makedirs(RAW, exist_ok=True)

    def win(self, title=None):
        c = cap.find(self.cls, title)
        if c is None:
            raise RuntimeError(f'no window {self.cls} {title}')
        return c

    def snap(self, name, marks=(), crop=None, title=None, cursor=False, region=None, scale=None):
        """Capture the app window (or an absolute region) and save lessons/<dir>/img/<name>.png."""
        c = None if region else self.win(title)
        x0, y0, w, h = region or cap.geom(c)
        raw = os.path.join(RAW, os.path.basename(os.path.dirname(self.dir)) + '__' + name + '.png')
        cap.shot(raw, c, region=region, cursor=cursor)

        def rel(m):
            m = dict(m)
            if 'box' in m:
                x, y, bw, bh = m['box']; m['box'] = (x - x0, y - y0, bw, bh)
                if 'badge_at' in m:
                    bx, by = m['badge_at']; m['badge_at'] = (bx - x0, by - y0)
            if 'pt' in m:
                x, y = m['pt']; m['pt'] = (x - x0, y - y0)
            if 'arrow' in m:
                a, b, cc, d = m['arrow']; m['arrow'] = (a - x0, b - y0, cc - x0, d - y0)
            if 'at' in m:
                x, y = m['at']; m['at'] = (x - x0, y - y0)
            return m

        cr = None
        if crop:
            cx, cy, cw, ch = crop
            cx, cy = max(cx - x0, 0), max(cy - y0, 0)
            cr = (cx, cy, min(cw, w - cx), min(ch, h - cy))
        out = os.path.join(self.dir, name + '.png')
        annotate(raw, out, [rel(m) for m in marks], crop=cr, scale=scale)
        return out
