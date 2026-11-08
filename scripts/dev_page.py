#!/usr/bin/env python3
"""Wrap app/index.html in the same skeleton the Artifact host adds, for local preview -> app/dev.html."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "app" / "index.html").read_text()
head = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}'
        'body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
(root / "app" / "dev.html").write_text(head + body + "</body></html>")
print("app/dev.html")
