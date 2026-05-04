# Runbook

## Service

- default port: 8096
- health: `GET /health`
- readiness: `GET /ready`
- ui: `GET /ui`

## Startup

```bash
pip install -r requirements-dev.txt
pip install -e .
python -m prompt_diff
```

## Smoke Checks

```bash
curl http://localhost:8096/health
curl http://localhost:8096/ready
curl http://localhost:8096/v1/diff -H "content-type: application/json" -d '{"baseline":"hello","candidate":"hello world"}'
```

## Incident Playbooks

### Diff endpoint latency spikes

1. Check request payload sizes.
2. Confirm max prompt limit is enforced.
3. Review upstream traffic burst/rate-limit settings.

### Unexpected high risk ratings

1. Compare added token list in response.
2. Review sensitive token set updates.
3. Validate placeholder removals in diff output.

### UI unavailable

1. Check frontend mount path and `PD_FRONTEND_DIR`.
2. Confirm static files present in deployed image.
