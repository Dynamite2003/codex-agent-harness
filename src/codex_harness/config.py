from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_PHASE_IDS = ["requirements", "design", "tasks", "implementation"]


@dataclass(frozen=True)
class CodexConfig:
    command: list[str]


@dataclass(frozen=True)
class PromptStyle:
    language: str = "zh-CN"
    tone: str = "direct"
    must_include: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class IsolationConfig:
    new_conversation_per_phase: bool = True
    artifact_only_context: bool = True


@dataclass(frozen=True)
class Phase:
    id: str
    title: str
    goal: list[str]
    input: list[str]
    output: list[str]
    steps: list[str]
    context_inputs: list[str]
    expected_outputs: list[str]


@dataclass(frozen=True)
class HarnessConfig:
    project_name: str
    workspace: str
    codex: CodexConfig
    isolation: IsolationConfig
    global_constraints: list[str]
    prompt_style: PromptStyle
    phases: list[Phase]


def load_config(path: Path) -> HarnessConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return parse_config(raw)


def parse_config(raw: dict[str, Any]) -> HarnessConfig:
    required = ["project_name", "workspace", "codex", "phases"]
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")

    command = raw["codex"].get("command")
    if not isinstance(command, list) or not all(isinstance(item, str) for item in command):
        raise ValueError("codex.command must be a list of strings")

    phases = [_parse_phase(item) for item in raw["phases"]]
    ids = [phase.id for phase in phases]
    duplicates = sorted({phase_id for phase_id in ids if ids.count(phase_id) > 1})
    if duplicates:
        raise ValueError(f"Duplicate phase ids: {', '.join(duplicates)}")
    if ids != REQUIRED_PHASE_IDS:
        raise ValueError(
            "phases must be exactly: "
            + ", ".join(REQUIRED_PHASE_IDS)
            + ". This harness always runs requirements -> design -> tasks -> implementation."
        )

    style_raw = raw.get("prompt_style", {})
    isolation_raw = raw.get("isolation", {})
    return HarnessConfig(
        project_name=str(raw["project_name"]),
        workspace=str(raw["workspace"]),
        codex=CodexConfig(command=command),
        isolation=IsolationConfig(
            new_conversation_per_phase=bool(isolation_raw.get("new_conversation_per_phase", True)),
            artifact_only_context=bool(isolation_raw.get("artifact_only_context", True)),
        ),
        global_constraints=list(raw.get("global_constraints", [])),
        prompt_style=PromptStyle(
            language=str(style_raw.get("language", "zh-CN")),
            tone=str(style_raw.get("tone", "direct")),
            must_include=list(style_raw.get("must_include", [])),
        ),
        phases=phases,
    )


def _parse_phase(raw: dict[str, Any]) -> Phase:
    required = ["id", "title", "goal", "input", "output", "steps"]
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"Missing required phase fields: {', '.join(missing)}")

    phase_id = str(raw["id"])
    if "/" in phase_id or phase_id in {".", ".."}:
        raise ValueError(f"Invalid phase id: {phase_id}")

    return Phase(
        id=phase_id,
        title=str(raw["title"]),
        goal=_string_list(raw["goal"]),
        input=_string_list(raw["input"]),
        output=_string_list(raw["output"]),
        steps=_string_list(raw["steps"]),
        context_inputs=list(raw.get("context_inputs", [])),
        expected_outputs=list(raw.get("expected_outputs", [])),
    )


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("phase prompt fields must be strings or lists of strings")
