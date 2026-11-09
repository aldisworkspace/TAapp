# TA App

Личная лента новостей, которая учит, как устроены сферы и как они влияют друг на друга: политика, международка, экономика, финансы, технологии, энергетика, медиа, искусство.

- Приложение: страница-артефакт (адрес в `artifact-url.txt`), исходник `app/index.html`. Один файл, без сборки.
- Выпуски: `app/editions/<дата>.json`, список в `app/editions/index.json` (последние 14). Схема — `editions/SCHEMA.md`.
- Новый выпуск: `/brief` (`.claude/skills/brief/SKILL.md`).
- Прогресс автора хранится в базе артефакта (`state/progress`) и в localStorage как кэш. Claude только читает его.
- Локальная проверка: `python3 scripts/dev_page.py` → `app/dev.html` (та же обёртка, что добавляет хост артефакта), сервер `python3 -m http.server 8765 --directory app`.
- Стандарт: каждая история с источниками; шаги механизма помечены fact / inference; ничего не выдумывать.
- Сайт: GitHub Pages из репозитория aldisworkspace/TAapp, собирается автоматически при каждом пуше в main (`.github/workflows/pages.yml` → `scripts/site_zip.py --site-only`). Иконки лежат в `assets/`.
