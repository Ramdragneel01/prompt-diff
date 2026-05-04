# Contributing

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
pytest
```

## Expectations

- Keep engine outputs deterministic.
- Add tests for any scoring or risk rule changes.
- Maintain compatibility between CLI/API/UI output fields.

## Pull Requests

- one focused change per PR
- include test evidence
- keep lint/tests green
