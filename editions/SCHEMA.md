# Edition schema (one JSON file per research batch, merged into editions/<date>.json)

{
  "stories": [
    {
      "id": "energy-opec-cut",             // kebab, unique
      "sphere": "energy",                  // politics | economy | arts | intl | finance | media | tech | energy
      "headline": "ОПЕК+ ...",             // RU, <= 70 chars, concrete, no hype
      "hook": "...",                       // RU, 1 sentence, the tension / why you should care, <= 120 chars
      "date": "2026-11-06",                // date of the event/publication
      "bigNumber": {"value": "$1.2 трлн", "label": "..."}, // optional, only a sourced number
      "facts": ["...", "..."],             // RU, 2-4 short atomic facts, each sourced (index into sources via [n])
      "mechanism": [                       // RU, 3-5 step causal chain; each step short (<= 90 chars)
        {"step": "...", "kind": "fact|inference"}
      ],
      "terms": [                           // 2-4 terms, term in EN, def in RU (<= 140 chars), in context of the story
        {"id": "term-kebab-id", "term": "Yield curve", "def": "..."}
      ],
      "links": [                           // 1-3 cross-sphere effects
        {"sphere": "finance", "text": "..."}   // RU, <= 110 chars, marked as inference implicitly
      ],
      "pattern": {"name": "...", "text": "..."}, // RU: the recurring pattern this is an instance of, <= 160 chars
      "quiz": {
        "q": "...",                        // RU, tests MECHANISM understanding, not trivia
        "options": ["...", "...", "...", "..."],
        "answer": 0,                       // index
        "why": "..."                       // RU, <= 160 chars
      },
      "predict": {"q": "...", "horizon": "2026-12-08"}, // optional yes/no question about the future, resolvable from public data
      "sources": [{"publisher": "Reuters", "title": "...", "url": "https://...", "date": "2026-11-06"}]
    }
  ]
}

## v2 additions (learning + visuals). All optional for the app, required for /brief from 2026-11-08 on.

"visual": ONE of the shapes below. Every number must come from the story's sources (src = 1-based index). No sourced numbers -> use "timeline" built from dated facts, or omit.
  {"type":"bars","title":"Экспорт нефти Казахстана, 2025","unit":"млн т","items":[{"label":"КТК","value":64.8},{"label":"Атырау–Самара","value":9.2,"hl":true}],"note":"Оба маршрута идут через Россию","src":1}
      2-5 items, same unit, "hl": true marks the one the story is about.
  {"type":"change","title":"Ставка Банка Англии","unit":"%","from":{"label":"до 5 ноября","value":3.75},"to":{"label":"после","value":4.0},"src":1}
  {"type":"share","title":"Доля КТК в экспорте нефти","value":80,"label":"около 80% экспорта, 2025","src":1}   (value = percent 0-100)
  {"type":"timeline","title":"Как развивались события","items":[{"date":"2 ноя","label":"Удар по узлу, прокачка остановлена"},{"date":"3 ноя","label":"Прокачка возобновлена"}],"src":1}  (2-5 items)

"guess": generation-effect prompt inside the mechanism. The reader sees steps 0..at-1 and picks what comes next.
  {"at": 3, "options": ["<correct, short paraphrase of mechanism[at].step>", "<plausible wrong>", "<plausible wrong>"], "answer": 0}
  at >= 2, vary answer index, options <= 80 chars each.

"analogy": elaboration — where else this same pattern shows up, in a different sphere or era.
  {"text": "Так же было в 1973: ...", "kind": "fact|inference"}  (<= 180 chars; "fact" only for well-documented history)

# Library cards (app/library/<sphere>.json): evergreen explainers that keep the feed endless.
{"cards":[{
  "id": "economy-policy-rate",            // <sphere>-<kebab>
  "sphere": "economy",
  "kind": "concept" | "pattern" | "player",   // how a thing works / a recurring pattern / who a key actor is and what levers they hold
  "title": "Как ставка ЦБ доходит до твоей ипотеки",   // RU, <= 70 chars, concrete
  "lede": "...",                           // RU, 1-2 sentences, the core idea, <= 200 chars
  "steps": ["...", "...", "..."],          // 3-5 step causal chain, each <= 90 chars
  "example": {"text": "...", "year": "2022"},  // one real, well-documented historical example, <= 180 chars
  "terms": [{"id":"policy-rate","term":"Policy rate","def":"..."}],   // 1-3, EN term, RU def <= 140
  "links": [{"sphere":"finance","text":"..."}],   // 1-2 cross-sphere effects, <= 110
  "quiz": {"q":"...","options":["...","...","...","..."],"answer":2,"why":"..."},
  "sources": [{"publisher":"Federal Reserve","title":"...","url":"https://..."}]   // reference pages: central banks, IMF, OECD, IEA, Britannica, Wikipedia, Investopedia
}]}
