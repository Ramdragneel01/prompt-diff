"""Prometheus metrics for prompt diff requests."""
from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

REQUESTS = Counter("prompt_diff_requests_total", "Total prompt diff requests", ["endpoint", "result"])


def mark_request(endpoint: str, result: str = "ok") -> None:
    REQUESTS.labels(endpoint=endpoint, result=result).inc()


def export_metrics() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
