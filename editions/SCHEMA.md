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
