#!/usr/bin/env python3
"""Build a standalone static copy of TA App for any web host -> dist/twin-angels/ and a zip.

Outside claude.ai there is no window.claude: progress lives in the browser (localStorage),
and Claude-powered features (Ask, explain-check, card generation, prediction verdicts) hide or fall back.
Usage: python3 scripts/site_zip.py            # folder + zip
       python3 scripts/site_zip.py --site-only  # folder only (GitHub Pages)
"""
import datetime, json, pathlib, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "app"
DIST = ROOT / "dist"
OUT = DIST / "twin-angels"

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Новости, которые учат: как устроены и связаны политика, экономика, финансы, технологии, энергетика, медиа и искусство.">
<meta name="theme-color" content="#07080C">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="TA App">
<meta property="og:type" content="website">
<meta property="og:title" content="TA App — новости, которые учат">
<meta property="og:description" content="Каждое утро — истории из восьми сфер с механизмом «причина → следствие», терминами и вопросом. Бесплатно, без регистрации.">
<meta property="og:url" content="https://taapp.nur.capital/">
<meta property="og:image" content="https://taapp.nur.capital/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<style>:root{color-scheme:dark}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""


README = """# TA App — приложение

Лента новостей, которая учит понимать, как устроены и связаны политика, международные отношения, экономика, финансы, технологии, энергетика, медиа и искусство. Каждая история: схема, «сначала база», карта участников, механизм «причина → следствие», термины, вопрос и объяснение своими словами. После новостей — библиотека из 120 карточек-основ и повторение терминов.

## Как залить
1. Распакуй архив. `index.html` лежит в корне.
2. Залей всё содержимое (кроме этого README, он не нужен на сайте) в корень сайта или поддомена, например `app.twinangels.nur.capital`. Можно и в подпапку — все пути относительные.
3. Нужен обычный статический хостинг. Сервер, база данных и ключи не нужны.

## Как установить на iPhone
1. Открой адрес сайта в Safari.
2. «Поделиться» → «На экран «Домой»» → «Добавить».
3. Иконка TA App откроет приложение на весь экран, без панели браузера.

## Что работает на обычном хостинге, а что нет
- Работает: все истории и схемы, словарь по нажатию на слово, вопросы, повторение терминов, серии, XP, карта связей, прогресс.
- Прогресс хранится в браузере этого устройства. На другом телефоне — с нуля. Если очистить данные Safari, прогресс пропадёт.
- Не работает (это функции claude.ai): «Спросить Claude», проверка объяснения Claude (вместо неё — сравнение с ключевыми мыслями), генерация новых карточек, сверка прогнозов. Эти кнопки на обычном хостинге скрыты.
- Новости не обновляются сами: это снимок на дату сборки. Новый архив собирается командой `python3 scripts/site_zip.py` в папке проекта после свежего выпуска.

## Состав
- `index.html` — приложение целиком (HTML, CSS, JS в одном файле).
- `editions/` — выпуски новостей, `library/` — карточки-основы, `glossary.json` — словарь.
- `manifest.webmanifest`, `icon-*.png` — установка на экран «Домой».
- Шрифты Golos Text и IBM Plex Mono подгружаются с Google Fonts.
"""


def icon(path, size):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, PathPatch
    from matplotlib.path import Path

    fig = plt.figure(figsize=(1, 1), dpi=size)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 24); ax.set_ylim(24, 0); ax.axis("off")
    fig.patch.set_facecolor("#07080C")
    cols = ["#FF7A6B", "#7B93FF", "#FFB547", "#3DDC97", "#AE9CFF", "#F2E14C", "#FF8FCF", "#4FE0D0"]
    for i, c in enumerate(cols):  # sphere mosaic band
        ax.add_patch(FancyBboxPatch((2.2 + i * 2.5, 19.2), 1.9, 1.9, boxstyle="round,pad=0,rounding_size=0.5", color=c, lw=0))
    verts = [(12, 16.5), (8.5, 14), (4.5, 11.5), (4.5, 6.5), (6.5, 6.5), (9.5, 7.3), (12, 10.8),
             (14.5, 7.3), (17.5, 6.5), (19.5, 6.5), (19.5, 11.5), (15.5, 14), (12, 16.5)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
             Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor="none", edgecolor="#F2F3F7", lw=size / 22, joinstyle="round"))
    fig.savefig(path, dpi=size, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    page = (APP / "index.html").read_text()
    (OUT / "index.html").write_text(HEAD + page + "\n</body>\n</html>\n")
    for sub in ("editions", "library"):
        shutil.copytree(APP / sub, OUT / sub)
    shutil.copy(APP / "glossary.json", OUT / "glossary.json")
    shutil.copy(APP / "sw.js", OUT / "sw.js")
    assets = ROOT / "assets"
    for s in (180, 192, 512):
        src = assets / f"icon-{s}.png"
        if src.exists():
            shutil.copy(src, OUT / src.name)
        else:  # first run on a machine with matplotlib: create and keep the icons in the repo
            assets.mkdir(exist_ok=True)
            icon(src, s)
            shutil.copy(src, OUT / src.name)
    if (assets / "og.png").exists():
        shutil.copy(assets / "og.png", OUT / "og.png")
    (OUT / "manifest.webmanifest").write_text(json.dumps({
        "name": "TA App", "short_name": "TA App", "lang": "ru", "id": "./",
        "description": "Новости, которые учат: как устроены и связаны политика, экономика, финансы, технологии, энергетика, медиа и искусство.",
        "categories": ["education", "news"],
        "start_url": "./", "scope": "./", "display": "standalone",
        "background_color": "#07080C", "theme_color": "#07080C",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]
    }, ensure_ascii=False, indent=1))
    if "--site-only" in sys.argv:  # used by GitHub Actions: just the folder, no README, no zip
        print(f"{OUT} ready")
        return
    (OUT / "README.md").write_text(README)
    stamp = datetime.date.today().isoformat()
    zpath = DIST / f"ta-app-{stamp}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(OUT))  # index.html at the zip root
    n = sum(1 for f in OUT.rglob("*") if f.is_file())
    print(f"{zpath} ({zpath.stat().st_size // 1024} KB, {n} files)")


if __name__ == "__main__":
    main()
