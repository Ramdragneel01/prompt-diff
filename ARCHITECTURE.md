# Architecture

## Objective

Provide deterministic and explainable prompt-diffing signals for both humans and automation pipelines.

## Components

- Tokenizer (`tokenizer.py`)
  - token extraction
  - placeholder detection
  - sentence chunking
- Semantic metrics (`semantic.py`)
  - lexical similarity (SequenceMatcher)
  - token Jaccard
  - change ratio
  - overlap ratio
- Risk module (`risk.py`)
  - sensitive token deltas
  - placeholder removal impact
  - risk level classification
- Engine (`engine.py`)
  - composes metrics + risk + unified diff
- API (`app.py`)
  - `/v1/diff` plus health/ready/metrics
- CLI (`cli.py`)
  - text/json output for local + CI usage
- UI (`frontend/*`)
  - interactive compare for manual review

## Data Flow

1. Input prompts enter via API, CLI, or UI.
2. Engine computes lexical/semantic and structural deltas.
3. Risk module scores potential safety/regression concerns.
4. Unified diff and structured payload are returned.

## Design Decisions

- Explainability first: no opaque embeddings in v0.1 path.
- Determinism: identical inputs always produce identical outputs.
- Multi-surface delivery: API/CLI/UI reuse same engine.
