# Урок 7. Препрес: підготовка до друку

**Програми:** Krita 6, Scribus 1.6

**Препрес** (додрукарська підготовка) — останній етап перед друкарнею. Мета уроку: отримати файли, які можна **без змін** відправити в друкарню, і заповнити заявку. Самого друку на воркшопі немає.

| Плакат для друкарні | Візитівки: розкладка на A4 |
|---|---|
| ![](img/result-poster-print.png) | ![](img/result-rozkladka-vizytivky.png) |

## Що потрібно перед початком

- `visual/keyvisual.kra` (урок 5), `poster/poster.sla` і `flyer/flyer.sla` (урок 6), `card/card-print.pdf` (урок 4).
- ICC-профіль {{asset icc/FOGRA39L_coated.icc}} (для Krita). У Scribus аналогічний профіль ISO Coated v2 вбудований.
- Шаблони {{asset templates/rozkladka-vizytivky.sla}}, {{asset templates/rozkladka-lystivky.sla short}}, {{asset templates/zaiavka-a4.svg short}}.

## Підуроки

| № | Тема | Що робимо |
|---|---|---|
| 7.1 | [Теорія: CMYK, PDF/X, розкладка](01-teoriia.md) | Колірне охоплення, рамки PDF, спуск полос, екологія друку |
| 7.2 | [Екранна кольоропроба в Krita](02-krita-kolorproba.md) | Профіль друку, кольоропроба, попередження про охоплення |
| 7.3 | [Кольоропроба й перевірка в Scribus](03-scribus-perevirka.md) | Керування кольором, Preflight Verifier |
| 7.4 | [PDF/X для друкарні](04-pdfx.md) | `poster-print.pdf` з мітками обрізу, `flyer-print.pdf` |
| 7.5 | [Розкладка](05-rozkladka.md) | 10 візитівок на A4, 2 листівки на SRA4 |
| 7.6 | [Заявка до друкарні](06-zaiavka.md) | Формат, папір, кольоровість, тираж, вартість |

## Результат уроку

| Файл | Що це |
|---|---|
| `poster/poster-print.pdf` | Плакат A4, PDF/X-4, вильоти 3 мм, мітки обрізу |
| `flyer/flyer-print.pdf` | Листівка A5, 2 сторінки, PDF/X-4, вильоти 3 мм |
| `print/rozkladka-vizytivky.pdf` | 10 візитівок на A4 (лицьовий і зворотний бік) з мітками обрізу |
| `print/rozkladka-lystivky.pdf` | 2 листівки на SRA4 з мітками обрізу |
| `print/zaiavka.svg` (або `.pdf`) | Заповнена заявка до друкарні |

## Критерії оцінювання

- Файли для друку: PDF/X, вильоти, мітки обрізу, перевірка перед друком без помилок: **0–2 бали**.
- Розрахунок розкладки й орієнтовної вартості в заявці: **0–1 бал**.

> На macOS замість `Ctrl` натискайте `Cmd`, а замість `Alt` — `Option`.

[← Урок 6](../06-verstka/README.md) · [Урок 8: Пітч →](../08-pitch/README.md)
