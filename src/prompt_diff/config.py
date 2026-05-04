"""Settings for prompt-diff service and CLI defaults."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PD_", env_file=".env", extra="ignore")

    service_name: str = "prompt-diff"
    host: str = "0.0.0.0"
    port: int = 8096
    log_level: str = "INFO"

    frontend_dir: str = "frontend"
    max_prompt_chars: int = Field(20000, ge=256, le=100000)
