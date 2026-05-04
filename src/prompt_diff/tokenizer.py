"""Tokenization and placeholder extraction utilities."""
from __future__ import annotations

import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-zA-Z0-9_']+")
PLACEHOLDER_RE = re.compile(r"\{\{?\s*[a-zA-Z0-9_\.:-]+\s*\}\}?")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def token_counter(text: str) -> Counter:
    return Counter(tokenize(text))


def extract_placeholders(text: str) -> list[str]:
    seen = []
    for m in PLACEHOLDER_RE.finditer(text):
        item = m.group(0).replace(" ", "")
        if item not in seen:
            seen.append(item)
    return seen


def sentence_chunks(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    return parts if parts else [text.strip()]
