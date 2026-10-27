"""Scribus script: build the example KavoBus poster (A4) and flyer (A5 x2 on A4).

Run:  scribus -g -ns -py tools/build_poster.py <workdir> [poster] [flyer]
Produces <workdir>/poster/poster.sla and <workdir>/flyer/flyer.sla
"""
import os, sys
import scribus as S

W = sys.argv[1]
KV = os.path.join(W, 'visual', 'keyvisual.png')
LOGO = os.path.join(W, 'logo', 'logo.svg')
LOGO_PNG = os.path.join(W, 'logo', 'logo.png')
QR = os.path.join(W, 'card', 'qr.png')

CREAM, BROWN, ORANGE = 'Kavobus Cream', 'Kavobus Brown', 'Kavobus Orange'
PT = 72 / 25.4  # setCornerRadius takes whole points


def colors():
    S.defineColorRGB(CREAM, 0xF3, 0xE9, 0xDC)
    S.defineColorRGB(BROWN, 0x4A, 0x2C, 0x2A)
    S.defineColorRGB(ORANGE, 0xE0, 0x7A, 0x2F)


def styles():
    S.createCharStyle(name='Head', font='Unbounded Bold', fontsize=40, fillcolor=CREAM)
    S.createParagraphStyle(name='Заголовок', linespacingmode=0, linespacing=44, alignment=0, charstyle='Head')
    S.createCharStyle(name='Sub', font='Montserrat Bold', fontsize=16, fillcolor=ORANGE)
    S.createParagraphStyle(name='Підзаголовок', linespacingmode=0, linespacing=20, alignment=0, charstyle='Sub')
    S.createCharStyle(name='Body', font='Montserrat Regular', fontsize=12, fillcolor=CREAM)
    S.createParagraphStyle(name='Текст', linespacingmode=0, linespacing=17, alignment=0, charstyle='Body')
    S.createCharStyle(name='CTA', font='Montserrat Bold', fontsize=14, fillcolor=BROWN)
    S.createParagraphStyle(name='Заклик', linespacingmode=0, linespacing=18, alignment=1, charstyle='CTA')


def text(x, y, w, h, txt, style, name):
    t = S.createText(x, y, w, h, name)
    S.setText(txt, t)
    S.setParagraphStyle(style, t)
    S.setTextDistances(0, 0, 0, 0, t)
    return t


def image(x, y, w, h, path, name):
    i = S.createImage(x, y, w, h, name)
    S.loadImage(path, i)
    S.setScaleImageToFrame(True, True, i)
    return i


def poster():
    S.newDocument((210, 297), (10, 10, 10, 10), S.PORTRAIT, 1, S.UNIT_MILLIMETERS, S.PAGE_1, 0, 1)
    S.setBleeds(3, 3, 3, 3)
    colors(); styles()
    image(-3, -3, 216, 303, KV, 'Ключовий візуал')
    # top shade for headline legibility
    r = S.createRect(-3, -3, 216, 135, 'Підкладка')
    S.setFillColor(BROWN, r); S.setFillTransparency(0.6, r); S.setLineColor('None', r)
    text(14, 18, 182, 60, 'Кава, що встигає з тобою', 'Заголовок', 'Заголовок')
    text(14, 82, 182, 10, 'Фургон «КавоБус» щоранку біля входу до коледжу', 'Підзаголовок', 'Підзаголовок')
    text(14, 96, 120, 30, 'Еспресо, лате, капучино — за 2 хвилини\rЗнижка 10 % для студентів\rПрацюємо з 7:30 до 16:00',
         'Текст', 'Переваги')
    # CTA button
    b = S.createRect(14, 255, 80, 14, 'Кнопка')
    S.setFillColor(ORANGE, b); S.setLineColor('None', b); S.setCornerRadius(round(PT * 7), b)
    t = text(14, 259, 80, 8, 'Перша кава — безкоштовно', 'Заклик', 'Заклик')
    # logo + qr on cream plate
    p = S.createRect(120, 250, 80, 37, 'Плашка')
    S.setFillColor(CREAM, p); S.setLineColor('None', p); S.setCornerRadius(round(PT * 3), p)
    image(124, 254, 50, 26.4, LOGO_PNG, 'Логотип')
    if os.path.exists(QR):
        image(177, 254, 20, 20, QR, 'QR-код')
    S.saveDocAs(os.path.join(W, 'poster', 'poster.sla'))
    S.closeDoc()


def flyer():
    # A5 flyer: 148 x 210
    S.newDocument((148, 210), (8, 8, 8, 8), S.PORTRAIT, 1, S.UNIT_MILLIMETERS, S.PAGE_1, 0, 2)
    S.setBleeds(3, 3, 3, 3)
    colors(); styles()
    # page 1: front
    image(-3, -3, 154, 216, KV, 'Фото')
    r = S.createRect(-3, 118, 154, 95, 'Фон')
    S.setFillColor(BROWN, r); S.setLineColor('None', r)
    text(10, 126, 128, 40, 'Кава, що встигає з тобою', 'Заголовок', 'Заголовок')
    S.setFontSize(26, 'Заголовок'); S.setLineSpacing(30, 'Заголовок')
    text(10, 170, 128, 20, 'Фургон «КавоБус» щоранку біля входу до коледжу', 'Підзаголовок', 'Підзаголовок')
    S.gotoPage(2)
    r2 = S.createRect(-3, -3, 154, 216, 'Фон 2')
    S.setFillColor(CREAM, r2); S.setLineColor('None', r2)
    image(39, 14, 70, 36.9, LOGO_PNG, 'Логотип')
    text(14, 62, 120, 10, 'Меню', 'Підзаголовок', 'Меню: заголовок')
    S.createCharStyle(name='Menu', font='Montserrat Regular', fontsize=14, fillcolor=BROWN)
    S.createParagraphStyle(name='Меню', linespacingmode=0, linespacing=22, alignment=0, charstyle='Menu')
    text(14, 74, 120, 40, 'Еспресо — 30 грн\rАмерикано — 35 грн\rКапучино — 45 грн\rЛате — 50 грн\rКакао — 40 грн',
         'Меню', 'Меню')
    t = text(14, 118, 120, 8, 'Знижка 10 % за студентським квитком.', 'Текст', 'Знижка')
    S.setTextColor(BROWN, t)
    b = S.createRect(34, 134, 80, 14, 'Кнопка')
    S.setFillColor(ORANGE, b); S.setLineColor('None', b); S.setCornerRadius(round(PT * 7), b)
    t = text(34, 138, 80, 8, 'Перша кава — безкоштовно', 'Заклик', 'Заклик')
    S.setTextColor(CREAM, t)
    if os.path.exists(QR):
        image(14, 168, 22, 22, QR, 'QR-код')
    t = text(42, 172, 92, 16, 'Біля входу до коледжу, з 7:30\r@kavobus · +380 67 000 00 00', 'Текст', 'Контакти')
    S.setTextColor(BROWN, t)
    S.saveDocAs(os.path.join(W, 'flyer', 'flyer.sla'))
    S.closeDoc()


which = sys.argv[2:] or ['poster', 'flyer']
if 'poster' in which:
    poster()
if 'flyer' in which:
    flyer()
