"""Lexical and structural similarity metrics."""
from __future__ import annotations

from difflib import SequenceMatcher

from .tokenizer import token_counter


def lexical_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def token_jaccard(a: str, b: str) -> float:
    a_set = set(token_counter(a).keys())
    b_set = set(token_counter(b).keys())
    if not a_set and not b_set:
        return 1.0
    intersection = len(a_set & b_set)
    union = len(a_set | b_set)
    return intersection / union if union else 1.0


def change_ratio(a: str, b: str) -> float:
    return 1.0 - lexical_similarity(a, b)


def overlap_ratio(a_items: list[str], b_items: list[str]) -> float:
    a_set = set(a_items)
    b_set = set(b_items)
    if not a_set and not b_set:
        return 1.0
    denom = max(len(a_set), len(b_set))
    if denom == 0:
        return 1.0
    return len(a_set & b_set) / denom
