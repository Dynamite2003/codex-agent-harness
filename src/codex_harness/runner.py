from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import HarnessConfig, Phase
from .prompting import build_prompt


@dataclass(frozen=True)
class PhaseRun:
    phase_id: str
    prompt_file: Path
    context_file: Path
    command_file: Path
    command: list[str]
    prompt_stdin: bool
    expected_outputs: list[Path]


@dataclass(frozen=True)
class HarnessRun:
    run_id: str
    run_dir: Path
    phases: list[PhaseRun]


def create_run(
    *,
    config: HarnessConfig,
    user_goal: str,
    project_root: Path,
    execute: bool = False,
) -> HarnessRun:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = project_root / config.workspace / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    phase_runs: list[PhaseRun] = []
    for phase in config.phases:
        phase_run = _prepare_phase(
            config=config,
            phase=phase,
            user_goal=user_goal,
            project_root=project_root,
            run_dir=run_dir,
        )
        phase_runs.append(phase_run)
        if execute:
            _execute_phase_command(phase_run, cwd=project_root)
            _validate_phase_outputs(phase_run)
            _write_phase_status(phase_run, ok=True)

    manifest = {
        "run_id": run_id,
        "project_name": config.project_name,
        "project_root": str(project_root),
        "goal": user_goal,
        "isolation": {
            "new_conversation_per_phase": config.isolation.new_conversation_per_phase,
            "artifact_only_context": config.isolation.artifact_only_context,
        },
        "phases": [
            {
                "id": item.phase_id,
                "prompt_file": str(item.prompt_file),
                "context_file": str(item.context_file),
                "command_file": str(item.command_file),
                "command": item.command,
                "prompt_stdin": item.prompt_stdin,
                "expected_outputs": [str(path) for path in item.expected_outputs],
            }
            for item in phase_runs
        ],
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return HarnessRun(run_id=run_id, run_dir=run_dir, phases=phase_runs)


def _prepare_phase(
    *,
    config: HarnessConfig,
    phase: Phase,
    user_goal: str,
    project_root: Path,
    run_dir: Path,
) -> PhaseRun:
    phase_dir = run_dir / phase.id
    phase_dir.mkdir(parents=True, exist_ok=False)
    conversation_dir = phase_dir / "conversation"
    conversation_dir.mkdir(exist_ok=False)

    context_files = _resolve_context_files(project_root, phase.context_inputs)
    prompt = build_prompt(
        config=config,
        phase=phase,
        user_goal=user_goal,
        project_root=project_root,
        run_dir=run_dir,
        context_files=context_files,
    )
    prompt_file = phase_dir / "prompt.md"
    context_file = phase_dir / "context.json"
    command_file = phase_dir / "command.sh"
    expected_outputs = [_resolve_context_path(project_root, item) for item in phase.expected_outputs]
    command, prompt_stdin = _render_command(
        config.codex.command,
        prompt_file=prompt_file,
        phase_id=phase.id,
        phase_dir=phase_dir,
        conversation_dir=conversation_dir,
        run_dir=run_dir,
        project_root=project_root,
    )

    prompt_file.write_text(prompt, encoding="utf-8")
    context_file.write_text(
        json.dumps(
            {
                "phase_id": phase.id,
                "phase_title": phase.title,
                "context_inputs": phase.context_inputs,
                "resolved_context_files": [str(path) for path in context_files],
                "missing_context_files": [
                    item for item in phase.context_inputs if not _resolve_context_path(project_root, item).exists()
                ],
                "expected_outputs": [str(path) for path in expected_outputs],
                "conversation": {
                    "mode": "new_per_phase" if config.isolation.new_conversation_per_phase else "shared_allowed",
                    "directory": str(conversation_dir),
                    "artifact_only_context": config.isolation.artifact_only_context,
                },
                "prompt_shape": ["目标", "输入", "输出", "步骤"],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    command_text = shlex.join(command)
    if prompt_stdin:
        command_text += " < " + shlex.quote(str(prompt_file))
    command_file.write_text("#!/usr/bin/env bash\nset -euo pipefail\n" + command_text + "\n", encoding="utf-8")
    command_file.chmod(0o755)

    return PhaseRun(
        phase_id=phase.id,
        prompt_file=prompt_file,
        context_file=context_file,
        command_file=command_file,
        command=command,
        prompt_stdin=prompt_stdin,
        expected_outputs=expected_outputs,
    )


def _execute_phase_command(phase_run: PhaseRun, *, cwd: Path) -> None:
    if phase_run.prompt_stdin:
        prompt = phase_run.prompt_file.read_text(encoding="utf-8")
        subprocess.run(phase_run.command, cwd=cwd, input=prompt, text=True, check=True)
        return

    subprocess.run(phase_run.command, cwd=cwd, check=True)


def _validate_phase_outputs(phase_run: PhaseRun) -> None:
    missing = [path for path in phase_run.expected_outputs if not path.exists()]
    if missing:
        _write_phase_status(phase_run, ok=False, missing=missing)
        formatted = "\n".join(f"- {path}" for path in missing)
        raise RuntimeError(
            f"Phase '{phase_run.phase_id}' finished, but required output artifacts are missing:\n{formatted}"
        )


def _write_phase_status(phase_run: PhaseRun, *, ok: bool, missing: list[Path] | None = None) -> None:
    status_file = phase_run.prompt_file.parent / "status.json"
    status_file.write_text(
        json.dumps(
            {
                "phase_id": phase_run.phase_id,
                "ok": ok,
                "expected_outputs": [str(path) for path in phase_run.expected_outputs],
                "missing_outputs": [str(path) for path in missing or []],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def _resolve_context_files(project_root: Path, inputs: list[str]) -> list[Path]:
    resolved = []
    for item in inputs:
        candidate = _resolve_context_path(project_root, item)
        if candidate.exists():
            resolved.append(candidate)
    return resolved


def _resolve_context_path(project_root: Path, item: str) -> Path:
    path = Path(item)
    if path.is_absolute():
        return path
    return project_root / path


def _render_command(
    command_template: list[str],
    *,
    prompt_file: Path,
    phase_id: str,
    phase_dir: Path,
    conversation_dir: Path,
    run_dir: Path,
    project_root: Path,
) -> tuple[list[str], bool]:
    values = {
        "prompt_file": str(prompt_file),
        "prompt_stdin": "-",
        "phase_id": phase_id,
        "phase_dir": str(phase_dir),
        "conversation_dir": str(conversation_dir),
        "run_dir": str(run_dir),
        "project_root": str(project_root),
    }
    return [item.format(**values) for item in command_template], "{prompt_stdin}" in command_template
