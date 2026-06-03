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
    if not isinstance(raw, dict):
        raise ValueError("config must be a JSON object")

    required = ["project_name", "workspace", "codex", "phases"]
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")

    project_name = _required_string(raw, "project_name")
    workspace = _required_string(raw, "workspace")
    codex_raw = _required_mapping(raw, "codex")
    command = codex_raw.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
        raise ValueError("codex.command must be a list of strings")

    phases_raw = raw["phases"]
    if not isinstance(phases_raw, list) or not all(isinstance(item, dict) for item in phases_raw):
        raise ValueError("phases must be a list of objects")

    phases = [_parse_phase(item) for item in phases_raw]
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

    style_raw = _optional_mapping(raw, "prompt_style")
    isolation_raw = _optional_mapping(raw, "isolation")
    return HarnessConfig(
        project_name=project_name,
        workspace=workspace,
        codex=CodexConfig(command=command),
        isolation=IsolationConfig(
            new_conversation_per_phase=_optional_bool(
                isolation_raw,
                "new_conversation_per_phase",
                default=True,
                owner="isolation",
            ),
            artifact_only_context=_optional_bool(
                isolation_raw,
                "artifact_only_context",
                default=True,
                owner="isolation",
            ),
        ),
        global_constraints=_optional_string_list(raw, "global_constraints", default=[]),
        prompt_style=PromptStyle(
            language=_optional_string(style_raw, "language", default="zh-CN", owner="prompt_style"),
            tone=_optional_string(style_raw, "tone", default="direct", owner="prompt_style"),
            must_include=_optional_string_list(
                style_raw,
                "must_include",
                default=[],
                owner="prompt_style",
            ),
        ),
        phases=phases,
    )


def _parse_phase(raw: dict[str, Any]) -> Phase:
    required = ["id", "title", "goal", "input", "output", "steps"]
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"Missing required phase fields: {', '.join(missing)}")

    phase_id = _required_string(raw, "id", owner="phase")
    if "/" in phase_id or "\\" in phase_id or phase_id in {".", ".."}:
        raise ValueError(f"Invalid phase id: {phase_id}")

    return Phase(
        id=phase_id,
        title=_required_string(raw, "title", owner=f"phase {phase_id}"),
        goal=_prompt_string_list(raw["goal"], field=f"phase {phase_id}.goal"),
        input=_prompt_string_list(raw["input"], field=f"phase {phase_id}.input"),
        output=_prompt_string_list(raw["output"], field=f"phase {phase_id}.output"),
        steps=_prompt_string_list(raw["steps"], field=f"phase {phase_id}.steps"),
        context_inputs=_optional_string_list(raw, "context_inputs", default=[], owner=f"phase {phase_id}"),
        expected_outputs=_optional_string_list(raw, "expected_outputs", default=[], owner=f"phase {phase_id}"),
    )


def _prompt_string_list(value: Any, *, field: str) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError(f"{field} must be a string or list of strings")


def _required_string(raw: dict[str, Any], key: str, *, owner: str = "config") -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{owner}.{key} must be a non-empty string")
    return value


def _optional_string(
    raw: dict[str, Any],
    key: str,
    *,
    default: str,
    owner: str = "config",
) -> str:
    if key not in raw:
        return default
    value = raw[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{owner}.{key} must be a non-empty string")
    return value


def _required_mapping(raw: dict[str, Any], key: str, *, owner: str = "config") -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{owner}.{key} must be an object")
    return value


def _optional_mapping(raw: dict[str, Any], key: str, *, owner: str = "config") -> dict[str, Any]:
    if key not in raw:
        return {}
    value = raw[key]
    if not isinstance(value, dict):
        raise ValueError(f"{owner}.{key} must be an object")
    return value


def _optional_bool(
    raw: dict[str, Any],
    key: str,
    *,
    default: bool,
    owner: str = "config",
) -> bool:
    if key not in raw:
        return default
    value = raw[key]
    if not isinstance(value, bool):
        raise ValueError(f"{owner}.{key} must be a boolean")
    return value


def _optional_string_list(
    raw: dict[str, Any],
    key: str,
    *,
    default: list[str],
    owner: str = "config",
) -> list[str]:
    if key not in raw:
        return list(default)
    value = raw[key]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{owner}.{key} must be a list of strings")
    return value
