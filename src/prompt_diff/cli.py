"""CLI for prompt-diff."""
from __future__ import annotations

import argparse
from pathlib import Path

from .engine import diff_prompts


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Semantic and lexical diff for prompt revisions")
    p.add_argument("--base", required=True, help="Path to baseline prompt file")
    p.add_argument("--candidate", required=True, help="Path to candidate prompt file")
    p.add_argument("--format", choices=["text", "json"], default="text")
    return p


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    baseline = _read_file(args.base)
    candidate = _read_file(args.candidate)
    result = diff_prompts(baseline, candidate)

    if args.format == "json":
        print(result.model_dump_json(indent=2))
        return 0

    print(result.summary)
    print(f"Risk: {result.risk.level}")
    if result.risk.reasons:
        print("Reasons:")
        for reason in result.risk.reasons:
            print(f"- {reason}")

    print("\nUnified Diff:\n")
    print(result.unified_diff or "(no diff)")
    return 0
