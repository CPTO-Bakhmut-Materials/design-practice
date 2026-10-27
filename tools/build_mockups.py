"""Krita mockup templates: brand-day/mockups/mockup-stina.kra and mockup-stil.kra.

Every layer is a *file layer*, so the .kra holds no pixels: the photo, the soft shadows and the
student's designs are PNG/JPG files next to it. A student copies the folder, exports the designs
under the fixed names below (default export settings), and Krita shows them in place.

  mockup-stina.kra  wall photo + plakat-page001.png + lystivka-page001.png (Scribus Save as Image, prefix
                    plakat / lystivka, PNG, 72 dpi — Scribus itself appends -page001)
  mockup-stil.kra   table photo + vizytivka-1.png / vizytivka-2.png (Inkscape pages, 96 dpi)

Run: python3 tools/build_mockups.py [designs_dir]
With designs_dir (containing the four PNGs) it also renders filled examples into lessons/08-pitch/img.
"""
import os, sys, uuid, zipfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'brand-day', 'mockups')
PHOTOS = os.path.join(ROOT, 'brand-day', 'photos', '99-mokapy')
FONT = os.path.join(ROOT, 'brand-day', 'fonts', 'Montserrat', 'Montserrat-Bold.ttf')

# name, photo (1920 px Wikimedia thumbnail), canvas scale chosen so designs match the scene, [(file, x, y, w, h, placeholder label)]
MOCKUPS = [
    ('mockup-stina', 'stina.jpg', 1.547, [('plakat-page001.png', 230, 170, 595, 842, 'плакат A4\n595 × 842 px'),
                                        ('lystivka-page001.png', 2300, 420, 419, 595, 'листівка A5\n419 × 595 px')]),
    ('mockup-stil', 'stil-zverkhu.jpg', 0.727, [('vizytivka-1.png', 200, 790, 340, 189, 'візитівка\nлицьовий бік'),
                                                ('vizytivka-2.png', 600, 790, 340, 189, 'візитівка\nзворотний бік')]),
]


def placeholder(path, w, h, label):
    im = Image.new('RGB', (w, h), '#f3e9dc')
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), outline='#976d3c', width=max(2, w // 120))
    f = ImageFont.truetype(FONT, max(14, w // 14))
    d.multiline_text((w / 2, h / 2), label, font=f, fill='#4a2c2a', anchor='mm', align='center', spacing=8)
    im.save(path)


def shadow(size, slots, path):
    """Soft drop shadow under every slot: black with a blurred alpha mask."""
    a = Image.new('L', size, 0)
    d = ImageDraw.Draw(a)
    for _, x, y, w, h, _ in slots:
        off = max(4, w // 60)
        d.rectangle((x + off, y + off * 2, x + w + off, y + h + off * 2), fill=150)
    a = a.filter(ImageFilter.GaussianBlur(max(6, slots[0][3] // 25)))
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    im.putalpha(a)
    im.save(path)


def layer(name, source, x=0, y=0, opacity=255, op='normal', locked=0):
    return (f'<layer channelflags="" collapsed="0" colorlabel="0" compositeop="{op}" intimeline="0" '
            f'locked="{locked}" name="{name}" nodetype="filelayer" opacity="{opacity}" scale="0" '
            f'source="{source}" uuid="{{{uuid.uuid4()}}}" visible="1" x="{x}" y="{y}"/>')


def compose(size, photo, shadow_png, slots, folder):
    im = photo.convert('RGBA')
    sh = Image.open(shadow_png)
    im = Image.alpha_composite(im, Image.merge('RGBA', (*[Image.new('L', size, 0)] * 3, sh.getchannel('A'))))
    for f, x, y, w, h, _ in slots:
        im.alpha_composite(Image.open(os.path.join(folder, f)).convert('RGBA'), (x, y))
    return im.convert('RGB')


def build_kra(name, photo_file, scale, slots, designs=None):
    src = Image.open(os.path.join(PHOTOS, photo_file)).convert('RGB')
    size = (round(src.width * scale), round(src.height * scale))
    photo = src.resize(size, Image.LANCZOS)
    base = name.replace('mockup-', '')
    photo_name, shadow_name = f'{base}-foto.jpg', f'{base}-tin.png'
    photo.save(os.path.join(OUT, photo_name), quality=90)
    shadow(size, slots, os.path.join(OUT, shadow_name))
    for f, x, y, w, h, label in slots:
        placeholder(os.path.join(OUT, f), w, h, label)
    layers = [layer(f.replace('-page001', '').replace('.png', ''), f, x, y) for f, x, y, w, h, _ in reversed(slots)]
    layers += [layer('Тінь', shadow_name, locked=1), layer('Фото', photo_name, locked=1)]
    maindoc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               "<!DOCTYPE DOC PUBLIC '-//KDE//DTD krita 2.0//EN' 'http://www.calligra.org/DTD/krita-2.0.dtd'>\n"
               '<DOC xmlns="http://www.calligra.org/DTD/krita" editor="Krita" kritaVersion="6.0.3" syntaxVersion="2.0">\n'
               f' <IMAGE colorspacename="RGBA" description="" height="{size[1]}" mime="application/x-kra" name="{name}" '
               f'profile="sRGB-elle-V2-srgbtrc.icc" width="{size[0]}" x-res="72" y-res="72">\n'
               f'  <layers>\n   ' + '\n   '.join(layers) + '\n  </layers>\n </IMAGE>\n</DOC>\n')
    merged = compose(size, photo, os.path.join(OUT, shadow_name), slots, OUT)
    kra = os.path.join(OUT, name + '.kra')
    with zipfile.ZipFile(kra, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/x-krita')  # first and stored, as Krita expects
        z.writestr('maindoc.xml', maindoc, zipfile.ZIP_DEFLATED)
        z.writestr('documentinfo.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<document-info xmlns="http://www.calligra.org/DTD/document-info"><about><title>'
                   + name + '</title></about></document-info>\n', zipfile.ZIP_DEFLATED)
        for fn, im in (('mergedimage.png', merged), ('preview.png', merged.copy())):
            if fn == 'preview.png':
                im.thumbnail((256, 256))
            tmp = os.path.join(OUT, '.' + fn)
            im.save(tmp)
            z.write(tmp, fn, zipfile.ZIP_DEFLATED)
            os.remove(tmp)
    print(kra, size)
    if designs:
        img = os.path.join(ROOT, 'lessons', '08-pitch', 'img')
        os.makedirs(img, exist_ok=True)
        compose(size, photo, os.path.join(OUT, shadow_name), slots, designs).save(os.path.join(img, f'result-{name}.jpg'), quality=88)
    return size


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for m in MOCKUPS:
        build_kra(*m, designs=sys.argv[1] if len(sys.argv) > 1 else None)
