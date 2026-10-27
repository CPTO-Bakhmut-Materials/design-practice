"""Annotate screenshots: numbered markers, frames and arrows (red, readable on light and dark UI)."""
import os
from PIL import Image, ImageDraw, ImageFont

RED = (230, 30, 60)
FONT = os.path.join(os.path.dirname(__file__), '..', 'brand-day', 'fonts', 'Montserrat', 'Montserrat-Bold.ttf')


def _font(size):
    return ImageFont.truetype(FONT, size)


def frame(d, box, width=4):
    x, y, w, h = box
    d.rounded_rectangle((x - 3, y - 3, x + w + 3, y + h + 3), radius=6, outline=RED, width=width)


def badge(d, x, y, n, r=17):
    d.ellipse((x - r, y - r, x + r, y + r), fill=RED, outline=(255, 255, 255), width=3)
    f = _font(int(r * 1.15))
    d.text((x, y + 1), str(n), font=f, fill='white', anchor='mm')


def arrow(d, x1, y1, x2, y2, width=5):
    import math
    d.line((x1, y1, x2, y2), fill=RED, width=width)
    a = math.atan2(y2 - y1, x2 - x1)
    L = 22
    p1 = (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45))
    p2 = (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=RED)


def label(d, x, y, text, size=22):
    f = _font(size)
    l, t, r, b = d.textbbox((x, y), text, font=f)
    d.rounded_rectangle((l - 8, t - 6, r + 8, b + 6), radius=6, fill=RED)
    d.text((x, y), text, font=f, fill='white')


def annotate(src, dst=None, marks=(), crop=None, scale=None):
    """marks: list of dicts:
         {'box': (x,y,w,h), 'n': 1}            frame + numbered badge at top-left
         {'pt': (x,y), 'n': 2}                 badge centred on a point (click spot)
         {'arrow': (x1,y1,x2,y2)}
         {'text': 'label', 'at': (x,y)}
       Coordinates are in the source image's pixels. crop=(x,y,w,h) applied after drawing.
    """
    im = Image.open(src).convert('RGB')
    d = ImageDraw.Draw(im)
    for m in marks:
        if 'box' in m:
            frame(d, m['box'])
            if 'n' in m:
                x, y, w, h = m['box']
                bx, by = m.get('badge_at', (x - 6, y - 6))
                badge(d, max(bx, 20), max(by, 20), m['n'])
        elif 'pt' in m:
            x, y = m['pt']
            d.ellipse((x - 26, y - 26, x + 26, y + 26), outline=RED, width=4)
            if 'n' in m:
                badge(d, x + 30, y - 30, m['n'])
        elif 'arrow' in m:
            arrow(d, *m['arrow'])
        if 'text' in m:
            label(d, *m['at'], m['text'])
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    if scale:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    dst = dst or src
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, optimize=True)
    return dst


def redact(src, box, text='home', dst=None):
    """Cover a region (e.g. a path bar showing the real home path) with a flat field and neutral text."""
    im = Image.open(src).convert('RGB')
    d = ImageDraw.Draw(im)
    x, y, w, h = box
    d.rectangle((x, y, x + w, y + h), fill=(255, 255, 255), outline=(170, 170, 170))
    f = ImageFont.truetype(FONT.replace('Bold', 'Regular'), int(h * 0.55))
    d.text((x + 8, y + h / 2), text, font=f, fill=(30, 30, 30), anchor='lm')
    im.save(dst or src)
    return dst or src
