"""Pydantic contracts for diff requests and results."""
from __future__ import annotations

from pydantic import BaseModel, Field


class DiffRequest(BaseModel):
    baseline: str = Field(min_length=1)
    candidate: str = Field(min_length=1)


class DiffMetrics(BaseModel):
    lexical_similarity: float
    token_jaccard: float
    change_ratio: float
    placeholder_overlap: float


class RiskAssessment(BaseModel):
    level: str
    reasons: list[str]
    added_sensitive_keywords: list[str]


class DiffResponse(BaseModel):
    summary: str
    metrics: DiffMetrics
    placeholders_added: list[str]
    placeholders_removed: list[str]
    tokens_added: list[str]
    tokens_removed: list[str]
    unified_diff: str
    risk: RiskAssessment
