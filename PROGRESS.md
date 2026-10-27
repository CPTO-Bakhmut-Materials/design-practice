# Workshop materials — progress & resume guide

Last updated: 2026-10-20 (late evening). Overall ≈ 98 % done. All 8 lessons written. Open items: see «Final cleanup».
To resume: open Claude Code in this folder and say **"Read PROGRESS.md and continue building the lessons."**

## Goal (user's request)
Build comprehensive lessons for the 6-hour workshop «Бренд за день» described in [plan.md](lessons/plan.md):
- Lesson text in **Ukrainian**; screenshots of apps in **English UI**, menu names translated in text.
- Format: **Markdown + PNG**, one folder per lesson in `lessons/`, split into sublessons.
- Every action shown and mentioned with annotated screenshots (numbered red markers), theory explained with text + diagrams.
- OS-independent wording (assume students can manage files; mention Cmd/Option for macOS).
- Free software only: **Inkscape 1.4, Krita 6, Scribus 1.6**.
- All templates and assets pre-made in `brand-day/` (copied to student PCs).
- Students work individually; no printing in class — only preparing files for print.
- Running example brand: **«КавоБус»** (student folder `Kovalenko_KavoBus`), colors `#F3E9DC` cream, `#4A2C2A` brown, `#E07A2F` orange, accent `#976D3C`; fonts Unbounded Bold (headings) + Montserrat.

## Status by lesson

| Folder | Status |
|---|---|
| `lessons/01-vstup/` | ✅ done (README + 4 diagrams) |
| `lessons/02-bryf-i-mudbord/` | ✅ done (5 sublessons) |
| `lessons/03-lohotyp/` | ✅ done (9 sublessons) |
| `lessons/04-vizytivka/` | ✅ done (5 sublessons) |
| `lessons/05-kliuchovyi-vizual/` | ✅ done (7 sublessons, Krita) |
| `lessons/06-verstka/` | ✅ done (8 sublessons) |
| `lessons/07-prepres/` | ✅ done (6 sublessons) |
| `lessons/08-pitch/` | ✅ done (4 sublessons) |

### Lesson 6 — Плакат і листівка (Scribus) ✅
Done 2026-10-20: README + 8 sublessons, diagrams (`tools/diag/d06.py`), screenshots s-01…s-24 (+ s-11b), result images rendered from headless PDF export. Example `poster.sla` / `flyer.sla` (+ `card/qr.png`) copied to `brand-day/example/`.
Facts verified in UI: Ctrl+N dialog defaults to Letter/inches and margins may be unlinked; colors have no HEX field (RGB 0–255); backdrop opacity is **Transparency → Opacity**; corner radius in Properties → Shape; **Insert → Barcode** → QR inserts a vector group placed by click; Style Manager **Import** pulls styles from another .sla; copy/paste between docs carries styles + colors; context menu Locking → **Is Locked**; **Adjust Frame Height to Text** exists.
`build_poster.py`: `setCornerRadius` needs an int in points (silently failed with float).
Minor: s-09/s-10 show the older smaller button radius (7 pt); text and s-18 use 7 mm.

### Lesson 7 — Препрес ✅
Done 2026-10-20: README + 6 sublessons, diagrams `tools/diag/d07.py` (d-okhoplennia, d-pdf-ramky, d-rozkladka), new screenshots s-08…s-14 (PDF/X dialog tabs redacted, layout templates, preflight "placed PDF"), k-05/k-06 stray mark fixed, raw-*.png removed.
New assets: `brand-day/templates/rozkladka-vizytivky.sla` (10 cards on A4, 2 pages) and `rozkladka-lystivky.sla` (2 A5 on **SRA4** 320×225 — two A5 with bleeds don't fit A4), built by `tools/build_imposition.py` (frames link ../card/card-print.pdf, ../flyer/flyer-print.pdf; back pages use PDF page 2; colour management on so PDF/X is available). `brand-day/templates/zaiavka-a4.svg` + filled `example/print/zaiavka.svg` from `tools/build_zaiavka.py` (prices labelled as conditional). Example print PDFs copied to `brand-day/example/{poster,flyer,print}/`.
Gotchas: Scribus places PDFs by **ArtBox** — GUI PDF/X export sets ArtBox=MediaBox (bleed kept), headless `export_pdf.py` gives ArtBox=TrimBox, so `flyer-print.pdf` must come from the GUI export. Students must tick **Embed PDF & EPS files** to keep placed PDFs vector. `export_pdf.py` now accepts `--no-marks`.
Note for user: plan.md says flyers «по 2 на A4» and lists 2 mm bleed for poster/flyers — lessons use SRA4 and 3 mm.

### Lesson 8 — Пітч ✅
Done 2026-10-20: README + 4 sublessons (01-mokapy, 02-tsina, 03-pitch, 04-refleksiia), diagrams `tools/diag/d08.py` (d-mokap, d-pitch, d-tsina), screenshots s-01 (Scribus Save as Image), i-01 (Inkscape Export → Page), k-01/k-02 (Krita mockup + File Layer Properties), result-mockup-*.jpg.
Mockups: `tools/build_mockups.py` writes `brand-day/mockups/mockup-stina.kra` / `mockup-stil.kra` by hand-assembling the .kra zip (kritarunner is unusable here: X11/Qt6-bindings errors). All layers are **file layers** (relative `source=`), so students just export PNGs with fixed names next to the .kra: `plakat-page001.png`, `lystivka-page001.png` (Scribus appends -page001 itself; 72 dpi, PNG — default type is `cur`!), `vizytivka-1.png`/`-2.png` (Inkscape Export → Single File → Page, default 96 dpi = 340×189). Placeholders with those names ship in the folder. Verified opening in Krita 6.0.3.
Mockup photos `99-mokapy/stina.jpg`, `stil-zverkhu.jpg` = 1920 px Wikimedia thumbnails (originals were rate-limited); picks updated in photo_picks_wm.json. Price exercise: rate 200 грн/год (labelled conditional), 4.2 h → ≈1940 грн.
Gotcha: Inkscape CLI silently refuses to write into dot-folders (e.g. `.sandbox/…`) — export to scratchpad and move.

## Final cleanup ✅
`lessons/README.md` index added; plan.md links to it; all links/images verified, no raw-*.png left. All picked photos downloaded (fetch script now falls back to 1920 px thumbnails when originals are rate-limited). Remaining: plan.md still says flyers «по 2 на A4» and 2 mm bleed for poster/flyer in додаток Г (lessons use SRA4 / 3 mm) — ask user before changing.

## Assets (`brand-day/`)
- `fonts/` ✅ 8 families, Cyrillic verified, name tables fixed, OFL.txt each.
- `icc/FOGRA39L_coated.icc` ✅.
- `templates/` ✅ bryf-a4.svg, mudbord-a4.svg, vizytivka-90x50.svg, rozkladka-*.sla, zaiavka-a4.svg. `mockups/` ✅ (lesson 8).
- `photos/` ✅ all picks downloaded (65 MB), CREDITS.md complete. `tools/fetch_picks_wm.py` skips existing files, retries, falls back to 1920 px thumbnails.
- `example/` ✅ logo/, card/ (+qr.png), moodboard.svg, visual/keyvisual.png, poster/poster.sla, flyer/flyer.sla. poster-print.pdf, flyer-print.pdf, print/rozkladka-*.pdf, print/zaiavka.svg.


## Tooling (`tools/`)
- `cap.py` — Hyprland capture harness: `launch()` starts app on **workspace 2** with sandboxed HOME/config (`.sandbox/`, fonts symlinked), `show()`/`back()` switch workspaces (returns to the user's previous one), `click/drag/key/field/type_text` via **ydotool**, `shot()` via grim, `floatwin()` to float+resize dialogs. Menus close when switching workspaces → open menu and capture in the same `show()` session.
- `lesson.py` — `Session(lesson_dir, app_cls).snap(name, marks, crop, region)`; raw captures kept in `.sandbox/raw/`.
- `annotate.py` — red frames/numbered badges; `redact()` hides real home path in file dialogs (always redact `/home/vperus…` path bars!).
- `diag/common.py` + `d01..d05.py` — theory diagrams (SVG → PNG via Inkscape CLI). Add `d06.py`, `d07.py`, `d08.py`.
- `build_poster.py` — Scribus script generating example poster/flyer: `scribus -g -ns -py tools/build_poster.py <workdir>` (run with sandbox HOME/XDG env, `QT_QPA_PLATFORM=offscreen`). `newDocument` page size is in mm.
- `build_materials.py` — generates `lessons/01-vstup/materialy.md` (preview + download page for `brand-day/`) and the gitignored `lessons/01-vstup/materialy/` (symlink to brand-day, per-folder zips, thumbnails). Run before `mdbook build`; skips unchanged files.
- `assets_preprocessor.py` — mdBook preprocessor (`[preprocessor.assets]` in book.toml): `{{asset templates/bryf-a4.svg}}` (or `{{asset … short}}` for the bare name) → link + ⬇ download button. Folder paths (`photos/01-kavobus/`) link to the materials page section and download its zip. Use it wherever a lesson needs a `brand-day/` file; warns at build time if the file is missing.
- `export_pdf.py` — headless PDF/X-4 export with bleeds + crop marks.
- Photo scripts: `photo_candidates_wm.py`, `wm_thumbs.py` (contact sheets in `.sandbox/cand-wm/`), `fetch_picks_wm.py` + `photo_picks_wm.json`.

## Environment prerequisites to resume
- Installed: inkscape, krita, scribus, grim, ydotool, imagemagick, qrencode, zbar, poppler.
- Start ydotool daemon (separate terminal, keep open):
  `sudo ydotoold --socket-path=/run/user/1000/.ydotool_socket --socket-own=1000:1000`
- `cap.WS` defaults to 2; export `CAP_WS=9` (or any free workspace) if 2 is occupied. Add the windowrule for that workspace **before** `launch()` — Scribus ignored the exec `[workspace N silent]` rule and opened on the user's active workspace.
- Runtime Hyprland window rules (lost on Hyprland restart, re-add; use the same workspace as CAP_WS):
  `hyprctl keyword windowrule "workspace 2 silent, match:class ^(org.inkscape.Inkscape)$"` (same for `krita`, `scribus`).
- Sandbox profile `.sandbox/` holds app configs (light themes, Krita soft-proof profile, Scribus panel layout) and the student work folder `.sandbox/home/Kovalenko_KavoBus/`.
- Single monitor eDP-1 1920×1200; app window on ws 2 is at (3,33) 1914×1164.

## User preferences (also in Claude memory)
- Deliverables in Ukrainian, prompts in English.
- "Оператори" = profession 4113, standard PDF in `standards/`.

## mdBook (2026-10-25)
Repo converted to an mdBook: `book.toml` at root, source = `lessons/` (plan.md and standards/ moved there), TOC in `lessons/SUMMARY.md`, theme in `theme/` (brand.css re-skins light + coal themes; fonts bundled via theme/fonts/fonts.css, needs `hash-files = false`). Default `index` preprocessor disabled so `README.md` links keep working. Build: `mdbook build` → `book/` (gitignored).
