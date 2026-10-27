# Бренд за день

Матеріали шестигодинного воркшопу з фірмового стилю: план, покрокові уроки, шаблони й готовий приклад.

- `lessons/` — джерело книги mdBook (уроки; `plan.md` — план для викладача, у книгу не входить)
- `brand-day/` — матеріали для комп'ютерів здобувачів
- `tools/` — скрипти для скриншотів, діаграм і прикладів
- `theme/` — тема книги в кольорах «КавоБус» і шрифти Unbounded + Montserrat

## Збірка книги

```sh
python3 tools/build_materials.py  # сторінка «Матеріали воркшопу»: прев’ю й архіви brand-day/ (потрібні Inkscape, poppler, Pillow)
mdbook build        # результат у book/, відкрийте book/index.html
mdbook serve --open # перегляд з автооновленням
```

Зміст книги — у `lessons/SUMMARY.md`; новий підурок треба додати туди.

## Публікація на GitHub Pages

Книгу збирає й публікує `.github/workflows/pages.yml` після кожного push у `main`.
Прев’ю й сторінку матеріалів (`lessons/01-vstup/materialy*`) треба зібрати локально й закомітити:
після змін у `brand-day/` запустіть `python3 tools/build_materials.py`. Архіви `zip/` збираються на GitHub.
Один раз увімкніть у репозиторії: **Settings → Pages → Source: GitHub Actions**.
