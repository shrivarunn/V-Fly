import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = {
    "base_url": "http://127.0.0.1:5173", "browser": "chrome",
    "explicit_wait_timeout": 10, "page_load_timeout": 30, "headless": False,
    "screenshot_dir": "artifacts/screenshots", "log_dir": "artifacts/logs",
    "html_report": "reports/pytest-report.html"
}
ENV_MAP = {
    "base_url": "TRIPTRAIL_BASE_URL", "browser": "TRIPTRAIL_BROWSER",
    "explicit_wait_timeout": "TRIPTRAIL_WAIT_TIMEOUT", "page_load_timeout": "TRIPTRAIL_PAGELOAD_TIMEOUT",
    "headless": "TRIPTRAIL_HEADLESS", "screenshot_dir": "TRIPTRAIL_SCREENSHOT_DIR",
    "log_dir": "TRIPTRAIL_LOG_DIR", "html_report": "TRIPTRAIL_HTML_REPORT"
}
def get_settings(overrides=None):
    settings = DEFAULTS.copy()
    config_path = ROOT / "config" / "settings.json"
    try:
        if config_path.exists():
            settings.update(json.loads(config_path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read configuration {config_path}: {exc}") from exc
    for key, env in ENV_MAP.items():
        if os.getenv(env) is not None:
            raw = os.environ[env]
            if key in ("explicit_wait_timeout", "page_load_timeout"):
                try: settings[key] = int(raw)
                except ValueError as exc: raise ValueError(f"{env} must be an integer") from exc
            elif key == "headless":
                settings[key] = raw.strip().lower() in ("1", "true", "yes", "on")
            else: settings[key] = raw
    if overrides:
        settings.update({k:v for k,v in overrides.items() if v is not None})
    if settings["browser"].lower() not in ("chrome", "edge"):
        raise ValueError("browser must be 'chrome' or 'edge'")
    for key in ("explicit_wait_timeout", "page_load_timeout"):
        if int(settings[key]) <= 0: raise ValueError(f"{key} must be greater than zero")
    settings["browser"] = settings["browser"].lower()
    for key in ("screenshot_dir", "log_dir", "html_report"):
        path = Path(settings[key])
        settings[key] = str(path if path.is_absolute() else ROOT / path)
    return settings
