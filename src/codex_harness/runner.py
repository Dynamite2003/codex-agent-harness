from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .config import HarnessConfig, Phase
from .prompting import build_prompt


@dataclass(frozen=True)
class PhaseRun:
    phase_id: str
    prompt_file: Path
    context_file: Path
    command_file: Path
    stdout_file: Path
    stderr_file: Path
    needs_user_input_file: Path
    command: list[str]
    prompt_stdin: bool
    expected_outputs: list[Path]


class PhaseNeedsUserInputError(RuntimeError):
    pass


@dataclass(frozen=True)
class HarnessRun:
    run_id: str
    run_dir: Path
    phases: list[PhaseRun]


UserInputProvider = Callable[[PhaseRun, str], str]


def create_run(
    *,
    config: HarnessConfig,
    user_goal: str,
    project_root: Path,
    execute: bool = False,
    user_input_provider: UserInputProvider | None = None,
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
            _execute_phase_until_ready(
                phase_run,
                cwd=project_root,
                user_input_provider=user_input_provider,
            )
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
                "stdout_file": str(item.stdout_file),
                "stderr_file": str(item.stderr_file),
                "needs_user_input_file": str(item.needs_user_input_file),
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
    stdout_file = phase_dir / "stdout.txt"
    stderr_file = phase_dir / "stderr.txt"
    needs_user_input_file = phase_dir / "needs-user-input.md"
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
        stdout_file=stdout_file,
        stderr_file=stderr_file,
        needs_user_input_file=needs_user_input_file,
        command=command,
        prompt_stdin=prompt_stdin,
        expected_outputs=expected_outputs,
    )


def _execute_phase_until_ready(
    phase_run: PhaseRun,
    *,
    cwd: Path,
    user_input_provider: UserInputProvider | None,
) -> None:
    while True:
        output = _execute_phase_command(phase_run, cwd=cwd)
        request = _detect_user_input_request(output)
        if not request:
            return
        if user_input_provider is None:
            _stop_for_user_input(phase_run, request)

        phase_run.needs_user_input_file.write_text(request.strip() + "\n", encoding="utf-8")
        answer = user_input_provider(phase_run, request)
        if not answer.strip():
            _stop_for_user_input(phase_run, request)
        _record_user_input_answer(phase_run, request=request, answer=answer)


def _execute_phase_command(phase_run: PhaseRun, *, cwd: Path) -> str:
    if phase_run.prompt_stdin:
        prompt = phase_run.prompt_file.read_text(encoding="utf-8")
        completed = subprocess.run(
            phase_run.command,
            cwd=cwd,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
        )
    else:
        completed = subprocess.run(phase_run.command, cwd=cwd, text=True, capture_output=True, check=False)

    phase_run.stdout_file.write_text(completed.stdout or "", encoding="utf-8")
    phase_run.stderr_file.write_text(completed.stderr or "", encoding="utf-8")
    completed.check_returncode()
    return "\n".join(part for part in [completed.stdout, completed.stderr] if part)


def _stop_for_user_input(phase_run: PhaseRun, request: str) -> None:
    phase_run.needs_user_input_file.write_text(request.strip() + "\n", encoding="utf-8")
    _write_phase_status(phase_run, ok=False, needs_user_input=True)
    raise PhaseNeedsUserInputError(
        "Phase "
        f"'{phase_run.phase_id}' requested user input. Harness stopped before the next phase.\n"
        f"Questions were written to: {phase_run.needs_user_input_file}\n"
        f"Full stdout: {phase_run.stdout_file}\n"
        f"Full stderr: {phase_run.stderr_file}"
    )


def _record_user_input_answer(phase_run: PhaseRun, *, request: str, answer: str) -> None:
    phase_dir = phase_run.prompt_file.parent
    answers_file = phase_dir / "user-answers.md"
    existing = answers_file.read_text(encoding="utf-8") if answers_file.exists() else ""
    round_number = existing.count("## Clarification Round") + 1
    block = (
        f"## Clarification Round {round_number}\n\n"
        "### Codex Questions\n\n"
        f"{request.strip()}\n\n"
        "### User Answers\n\n"
        f"{answer.strip()}\n"
    )
    answers_file.write_text((existing + "\n" if existing else "") + block + "\n", encoding="utf-8")

    prompt = phase_run.prompt_file.read_text(encoding="utf-8").rstrip()
    prompt += (
        "\n\n补充用户回答：\n"
        f"以下是第 {round_number} 轮用户对你上一轮问题的回答。请基于这些回答继续完成当前阶段；"
        "如果仍然缺少关键决策，可以再次输出 HARNESS_NEEDS_USER_INPUT 并列出问题；"
        "否则生成当前阶段要求的 artifact。\n\n"
        f"{answer.strip()}\n"
    )
    phase_run.prompt_file.write_text(prompt + "\n", encoding="utf-8")
    if phase_run.needs_user_input_file.exists():
        phase_run.needs_user_input_file.unlink()


def _detect_user_input_request(output: str) -> str | None:
    text = output.strip()
    if not text:
        return None

    marker = "HARNESS_NEEDS_USER_INPUT"
    if marker in text:
        return text[text.index(marker) :]

    lowered = text.lower()
    question_markers = [
        "请确认",
        "请你确认",
        "请回答",
        "请提供",
        "需要你",
        "需要您",
        "需要用户",
        "需要确认",
        "需要补充",
        "待你确认",
        "待用户确认",
        "有几个问题",
        "以下问题",
        "before i continue",
        "before proceeding",
        "please confirm",
        "please provide",
        "need your input",
        "need clarification",
    ]
    if any(marker in lowered for marker in question_markers):
        return text
    return None


def _validate_phase_outputs(phase_run: PhaseRun) -> None:
    missing = [path for path in phase_run.expected_outputs if not path.exists()]
    if missing:
        _write_phase_status(phase_run, ok=False, missing=missing)
        formatted = "\n".join(f"- {path}" for path in missing)
        raise RuntimeError(
            f"Phase '{phase_run.phase_id}' finished, but required output artifacts are missing:\n{formatted}"
        )


def _write_phase_status(
    phase_run: PhaseRun,
    *,
    ok: bool,
    missing: list[Path] | None = None,
    needs_user_input: bool = False,
) -> None:
    status_file = phase_run.prompt_file.parent / "status.json"
    status_file.write_text(
        json.dumps(
            {
                "phase_id": phase_run.phase_id,
                "ok": ok,
                "needs_user_input": needs_user_input,
                "needs_user_input_file": str(phase_run.needs_user_input_file) if needs_user_input else None,
                "expected_outputs": [str(path) for path in phase_run.expected_outputs],
                "missing_outputs": [str(path) for path in missing or []],
                "stdout_file": str(phase_run.stdout_file),
                "stderr_file": str(phase_run.stderr_file),
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
