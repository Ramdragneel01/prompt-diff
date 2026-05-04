"""Risk assessment for prompt deltas."""
from __future__ import annotations

from .tokenizer import tokenize

SENSITIVE_TOKENS = {
    "jailbreak",
    "bypass",
    "ignore",
    "override",
    "secrets",
    "credentials",
    "password",
    "api_key",
    "token",
    "system_prompt",
    "shell",
    "sudo",
    "exfiltrate",
}


def assess_risk(
    lexical_similarity: float,
    placeholders_removed: list[str],
    baseline: str,
    candidate: str,
) -> tuple[str, list[str], list[str]]:
    baseline_tokens = set(tokenize(baseline))
    candidate_tokens = set(tokenize(candidate))
    added = sorted((candidate_tokens - baseline_tokens) & SENSITIVE_TOKENS)

    reasons: list[str] = []
    if lexical_similarity < 0.45:
        reasons.append("Large semantic drift between baseline and candidate prompt")
    if placeholders_removed:
        reasons.append("Placeholder removals may break runtime interpolation")
    if added:
        reasons.append("Sensitive/dangerous instruction keywords introduced")

    if added or lexical_similarity < 0.35:
        level = "high"
    elif reasons:
        level = "medium"
    else:
        level = "low"

    return level, reasons, added
