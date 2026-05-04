"""Core diff engine combining lexical, structural, and risk signals."""
from __future__ import annotations

import difflib

from .models import DiffMetrics, DiffResponse, RiskAssessment
from .risk import assess_risk
from .semantic import change_ratio, lexical_similarity, overlap_ratio, token_jaccard
from .tokenizer import extract_placeholders, token_counter


def _delta_tokens(baseline: str, candidate: str) -> tuple[list[str], list[str]]:
    base_counts = token_counter(baseline)
    cand_counts = token_counter(candidate)

    added: list[str] = []
    removed: list[str] = []

    for tok, count in cand_counts.items():
        extra = count - base_counts.get(tok, 0)
        if extra > 0:
            added.extend([tok] * extra)

    for tok, count in base_counts.items():
        extra = count - cand_counts.get(tok, 0)
        if extra > 0:
            removed.extend([tok] * extra)

    return sorted(added), sorted(removed)


def diff_prompts(baseline: str, candidate: str) -> DiffResponse:
    lex = lexical_similarity(baseline, candidate)
    jac = token_jaccard(baseline, candidate)
    cr = change_ratio(baseline, candidate)

    base_ph = extract_placeholders(baseline)
    cand_ph = extract_placeholders(candidate)
    overlap = overlap_ratio(base_ph, cand_ph)

    placeholders_added = sorted(set(cand_ph) - set(base_ph))
    placeholders_removed = sorted(set(base_ph) - set(cand_ph))

    tokens_added, tokens_removed = _delta_tokens(baseline, candidate)

    unified = "\n".join(
        difflib.unified_diff(
            baseline.splitlines(),
            candidate.splitlines(),
            fromfile="baseline",
            tofile="candidate",
            lineterm="",
        )
    )

    risk_level, reasons, sensitive_added = assess_risk(
        lexical_similarity=lex,
        placeholders_removed=placeholders_removed,
        baseline=baseline,
        candidate=candidate,
    )

    summary = (
        f"Prompt changed with lexical similarity {lex:.3f}, token Jaccard {jac:.3f}, "
        f"and risk level {risk_level}."
    )

    return DiffResponse(
        summary=summary,
        metrics=DiffMetrics(
            lexical_similarity=lex,
            token_jaccard=jac,
            change_ratio=cr,
            placeholder_overlap=overlap,
        ),
        placeholders_added=placeholders_added,
        placeholders_removed=placeholders_removed,
        tokens_added=tokens_added,
        tokens_removed=tokens_removed,
        unified_diff=unified,
        risk=RiskAssessment(
            level=risk_level,
            reasons=reasons,
            added_sensitive_keywords=sensitive_added,
        ),
    )
