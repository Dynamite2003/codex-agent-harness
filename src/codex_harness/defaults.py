from __future__ import annotations

from importlib.resources import files


def default_config_text() -> str:
    text = files("codex_harness").joinpath("default.harness.json").read_text(encoding="utf-8")
    return text if text.endswith("\n") else text + "\n"
