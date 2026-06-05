from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillFlowInitResult:
    project_root: Path
    skills_source: Path
    skills_target: Path
    installed_skills: list[str]
    docs_created: list[Path]
    overwritten: list[Path]


def init_skill_flow(
    *,
    project_root: Path,
    codex_home: Path | None = None,
    force: bool = False,
    create_docs: bool = True,
) -> SkillFlowInitResult:
    project_root = project_root.resolve()
    codex_home = codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skills_source = _find_skills_source(project_root)
    skills_target = codex_home.expanduser().resolve() / "skills"
    skills_target.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    overwritten: list[Path] = []
    for source in sorted(path for path in skills_source.iterdir() if path.is_dir()):
        if not (source / "SKILL.md").exists():
            continue
        target = skills_target / source.name
        if target.exists():
            if not force:
                continue
            shutil.rmtree(target)
            overwritten.append(target)
        shutil.copytree(source, target)
        installed.append(source.name)

    docs_created = _create_flow_docs(project_root) if create_docs else []
    return SkillFlowInitResult(
        project_root=project_root,
        skills_source=skills_source,
        skills_target=skills_target,
        installed_skills=installed,
        docs_created=docs_created,
        overwritten=overwritten,
    )


def _find_skills_source(project_root: Path) -> Path:
    candidates = [
        Path(os.environ["CODEX_HARNESS_SKILLS_DIR"]).expanduser()
        if "CODEX_HARNESS_SKILLS_DIR" in os.environ
        else None,
        project_root / "skills",
        Path(__file__).resolve().parents[2] / "skills",
    ]
    for candidate in candidates:
        if candidate and (candidate / "vibe2spec-flow" / "SKILL.md").exists():
            return candidate.resolve()
    raise FileNotFoundError(
        "Unable to find bundled skills. Set CODEX_HARNESS_SKILLS_DIR to the repository skills directory."
    )


def _create_flow_docs(project_root: Path) -> list[Path]:
    created: list[Path] = []
    for directory in [project_root / "doc", project_root / "doc" / "specs", project_root / "doc" / "tasks"]:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(directory)

    quickstart = project_root / "doc" / "vibe2spec-quickstart.md"
    if not quickstart.exists():
        quickstart.write_text(_quickstart_text(), encoding="utf-8")
        created.append(quickstart)
    return created


def _quickstart_text() -> str:
    return """# Vibe2Spec Quickstart

默认日常使用轻量 skill，不需要启动完整 harness：

```text
$vibe2spec-flow <你的功能需求>
```

推荐流程：

1. 生成或更新 `doc/proposal.md`，用 EARS 写功能需求，用 ADR Candidates 记录关键决策，用 GIVEN-WHEN-THEN 写验收标准。
2. 生成或更新 `doc/detailed-design.md`，收敛 ADR，明确模块、契约、风险和测试策略。
3. 生成或更新 `doc/tasks/progress.md` 与 `doc/tasks/<module-name>.md`，标记 AFK/HITL、Blocked by 和验收标准。
4. 默认由单个 Codex agent 顺序实现并验证；只有任务独立、文件范围清晰且上下文明显过长时才可选启用子 agents。

需要完整审计、stdout/stderr、失败状态和阶段复跑时，再使用：

```bash
./harness -C . "你的功能需求"
```
"""
