#!/usr/bin/env python3
"""Merge editions/_raw/*.json into app/editions/<date>.json, validate, update index.

Usage: python3 scripts/build_edition.py 2026-11-08 [--title "..."]
Only stdlib. Fails loudly on schema problems so a broken edition never ships.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "editions" / "_raw"
OUT = ROOT / "app" / "editions"
SPHERES = {"politics", "intl", "economy", "finance", "tech", "energy", "arts", "media"}
ORDER = ["intl", "economy", "tech", "energy", "finance", "politics", "media", "arts"]


def check(s):
    errs = []
    need = ["id", "sphere", "headline", "hook", "date", "mechanism", "terms", "quiz", "sources"]
    for k in need:
        if not s.get(k):
            errs.append(f"missing {k}")
    if s.get("sphere") not in SPHERES:
        errs.append(f"bad sphere {s.get('sphere')}")
    q = s.get("quiz") or {}
    if not (isinstance(q.get("options"), list) and 2 <= len(q["options"]) <= 4 and 0 <= q.get("answer", -1) < len(q["options"])):
        errs.append("bad quiz")
    n = len(s.get("sources") or [])
    for src in s.get("sources") or []:
        if not str(src.get("url", "")).startswith("http"):
            errs.append("source without url")
    for f in s.get("facts") or []:
        for m in re.findall(r"\[(\d+)\]", f):
            if not 1 <= int(m) <= n:
                errs.append(f"fact ref [{m}] out of range")
    for m in s.get("mechanism") or []:
        if m.get("kind") not in ("fact", "inference"):
            errs.append("mechanism kind")
    v = s.get("visual")
    if v is not None:
        if v.get("type") not in ("bars", "change", "share", "timeline"):
            errs.append("bad visual type")
        if not 1 <= int(v.get("src", 0)) <= n:
            errs.append("visual src out of range")
    g = s.get("guess")
    if g is not None and not (1 <= g.get("at", 0) < len(s.get("mechanism") or []) and 0 <= g.get("answer", -1) < len(g.get("options") or [])):
        errs.append("bad guess")
    a = s.get("actors")
    if a is not None:
        ids = {n.get("id") for n in a.get("nodes") or []}
        if not 2 <= len(ids) <= 5 or any(e.get("from") not in ids or e.get("to") not in ids for e in a.get("edges") or []):
            errs.append("bad actors")
    for l in s.get("links") or []:
        if l.get("sphere") not in SPHERES:
            errs.append(f"bad link sphere {l.get('sphere')}")
    return errs


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    date = sys.argv[1]
    title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else None
    stories, seen, bad = [], set(), 0
    enrich = {}
    for p in sorted(RAW.glob("enrich*.json")):
        enrich.update(json.loads(p.read_text()))
    v3 = {}
    for p in sorted(RAW.glob("v3-*.json")):
        v3.update(json.loads(p.read_text()))
    for p in sorted(RAW.glob("*.json")):
        if p.name.startswith("enrich") or p.name.startswith("v3-"):
            continue
        for s in json.loads(p.read_text())["stories"]:
            s.update(enrich.get(s.get("id"), {}))
            x = dict(v3.get(s.get("id"), {}))
            qe = x.pop("quiz_explain", None)
            if x.get("mechanism") and len(x["mechanism"]) != len(s.get("mechanism") or []):
                x.pop("mechanism")  # never break the guess index
            s.update(x)
            if qe and s.get("quiz") and len(qe) == len(s["quiz"].get("options", [])):
                s["quiz"]["explain"] = qe
            e = check(s)
            if s.get("id") in seen:
                e.append("duplicate id")
            if e:
                bad += 1
                print(f"[{p.name}] {s.get('id')}: {'; '.join(e)}")
                continue
            seen.add(s["id"])
            stories.append(s)
    if bad:
        sys.exit(f"{bad} story(ies) failed validation; fix _raw and rerun")
    # interleave spheres so the feed never shows two of the same in a row when avoidable
    buckets = {k: [s for s in stories if s["sphere"] == k] for k in ORDER}
    mixed = []
    while any(buckets.values()):
        for k in ORDER:
            if buckets[k]:
                mixed.append(buckets[k].pop(0))
    OUT.mkdir(parents=True, exist_ok=True)
    ed = {"date": date, "stories": mixed}
    if title:
        ed["title"] = title
    (OUT / f"{date}.json").write_text(json.dumps(ed, ensure_ascii=False, indent=1))
    idx_p = OUT / "index.json"
    idx = json.loads(idx_p.read_text()) if idx_p.exists() else {"editions": []}
    if date not in idx["editions"]:
        idx["editions"].append(date)
    idx["editions"] = sorted(idx["editions"], reverse=True)[:14]
    idx_p.write_text(json.dumps(idx, indent=1))
    lib = ROOT / "app" / "library"
    if lib.exists():
        files = sorted(f.name for f in lib.glob("*.json") if f.name != "index.json")
        (lib / "index.json").write_text(json.dumps({"files": files}, indent=1))
    print(f"ok: {len(mixed)} stories -> app/editions/{date}.json; index has {len(idx['editions'])} editions")


if __name__ == "__main__":
    main()
