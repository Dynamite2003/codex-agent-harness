from __future__ import annotations

from pathlib import Path

from .config import HarnessConfig, Phase


def build_prompt(
    *,
    config: HarnessConfig,
    phase: Phase,
    user_goal: str,
    project_root: Path,
    run_dir: Path,
    context_files: list[Path],
) -> str:
    values = _template_values(
        phase=phase,
        user_goal=user_goal,
        project_root=project_root,
        run_dir=run_dir,
        context_files=context_files,
        config=config,
    )
    lines: list[str] = []
    lines.extend(_section("目标", phase.goal, values))
    lines.append("")
    input_items = list(phase.input)
    if config.isolation.new_conversation_per_phase:
        input_items.append(
            "对话隔离：这是 {phase_title} 阶段的新对话，不要依赖其他阶段的聊天历史；"
            "只能使用本 prompt 明确列出的输入和 artifact。"
        )
    lines.extend(_section("输入", input_items, values))
    lines.append("")
    lines.extend(_section("输出", phase.output, values))
    lines.append("")
    lines.extend(_section("步骤", phase.steps, values))

    return "\n".join(lines).strip() + "\n"


def _template_values(
    *,
    phase: Phase,
    user_goal: str,
    project_root: Path,
    run_dir: Path,
    context_files: list[Path],
    config: HarnessConfig,
) -> dict[str, str]:
    phase_dir = run_dir / phase.id
    context_text = _context_text(phase=phase, project_root=project_root, context_files=context_files)
    constraints_text = "\n".join(f"- {item}" for item in config.global_constraints) or "- 无"
    return {
        "user_goal": user_goal.strip(),
        "phase_id": phase.id,
        "phase_title": phase.title,
        "project_root": str(project_root),
        "run_dir": str(run_dir),
        "phase_dir": str(phase_dir),
        "conversation_dir": str(phase_dir / "conversation"),
        "context_files": context_text,
        "global_constraints": constraints_text,
        "conversation_policy": _conversation_policy(config),
    }


def _conversation_policy(config: HarnessConfig) -> str:
    if config.isolation.new_conversation_per_phase and config.isolation.artifact_only_context:
        return "每个阶段使用新的 Codex 对话，只通过声明的 artifact 传递上下文。"
    if config.isolation.new_conversation_per_phase:
        return "每个阶段使用新的 Codex 对话。"
    return "允许复用对话上下文。"


def _context_text(*, phase: Phase, project_root: Path, context_files: list[Path]) -> str:
    if not phase.context_inputs:
        return "- 无上游 artifact"

    existing = {path.resolve() for path in context_files}
    lines = []
    for item in phase.context_inputs:
        raw_path = Path(item)
        path = raw_path if raw_path.is_absolute() else project_root / raw_path
        status = "exists" if path.resolve() in existing else "missing"
        lines.append(f"- {path} ({status})")
    return "\n".join(lines)


def _section(title: str, items: list[str], values: dict[str, str]) -> list[str]:
    rendered = [_render_template(item, values) for item in items if item.strip()]
    if not rendered:
        rendered = ["无"]
    return [f"{title}：", *rendered]


def _render_template(template: str, values: dict[str, str]) -> str:
    try:
        return template.format(**values)
    except KeyError as error:
        missing = error.args[0]
        raise ValueError(f"Unknown prompt template variable: {missing}") from error
