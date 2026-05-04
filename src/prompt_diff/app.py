"""FastAPI service for prompt diffing."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from .config import Settings
from .engine import diff_prompts
from .metrics import export_metrics, mark_request
from .models import DiffRequest, DiffResponse


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="prompt-diff", version="0.1.0")

    @app.get("/")
    def root() -> dict:
        mark_request("root")
        return {"service": settings.service_name, "ui": "/ui", "docs": "/docs"}

    @app.get("/health")
    def health() -> dict:
        mark_request("health")
        return {"status": "ok", "service": settings.service_name}

    @app.get("/ready")
    def ready() -> dict:
        mark_request("ready")
        return {"status": "ready"}

    @app.get("/metrics")
    def metrics() -> Response:
        payload, content_type = export_metrics()
        return Response(content=payload, media_type=content_type)

    @app.post("/v1/diff", response_model=DiffResponse)
    def diff(payload: DiffRequest) -> DiffResponse:
        mark_request("diff")

        if len(payload.baseline) > settings.max_prompt_chars or len(payload.candidate) > settings.max_prompt_chars:
            mark_request("diff", "rejected")
            raise HTTPException(
                status_code=400,
                detail=f"Prompt exceeds max size ({settings.max_prompt_chars} chars)",
            )

        return diff_prompts(payload.baseline, payload.candidate)

    frontend_candidates = [
        Path(settings.frontend_dir),
        Path(__file__).resolve().parents[2] / settings.frontend_dir,
    ]
    frontend = next((path for path in frontend_candidates if path.exists()), None)
    if frontend is not None:
        app.mount("/ui", StaticFiles(directory=str(frontend), html=True), name="ui")

    return app


app = create_app()
