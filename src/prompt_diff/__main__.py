"""Entrypoint for prompt-diff CLI/API runtime."""
from __future__ import annotations

import sys

import uvicorn

from .cli import run_cli
from .config import Settings


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
        raise SystemExit(run_cli(sys.argv[1:]))

    settings = Settings()
    uvicorn.run(
        "prompt_diff.app:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
