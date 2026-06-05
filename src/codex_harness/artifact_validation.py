from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactValidationIssue:
    path: Path
    message: str


def validate_project_artifacts(project_root: Path) -> list[ArtifactValidationIssue]:
    project_root = project_root.resolve()
    issues: list[ArtifactValidationIssue] = []
    for relative in [
        "doc/proposal.md",
        "doc/detailed-design.md",
        "doc/tasks/progress.md",
        "doc/prompt.md",
    ]:
        path = project_root / relative
        if path.exists():
            issues.extend(validate_artifact(path, project_root=project_root))

    tasks_dir = project_root / "doc" / "tasks"
    if tasks_dir.exists():
        for path in sorted(tasks_dir.glob("*.md")):
            if path.name != "progress.md":
                issues.extend(validate_artifact(path, project_root=project_root))
    return issues


def validate_paths(paths: list[Path], *, project_root: Path) -> list[ArtifactValidationIssue]:
    issues: list[ArtifactValidationIssue] = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.glob("*.md")):
                issues.extend(validate_artifact(child, project_root=project_root))
        elif path.exists():
            issues.extend(validate_artifact(path, project_root=project_root))
    return issues


def validate_artifact(path: Path, *, project_root: Path) -> list[ArtifactValidationIssue]:
    relative = _relative(path, project_root)
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    if relative == "doc/proposal.md":
        return _validate_tokens(
            path,
            text,
            [
                ("Context", ["context", "背景"]),
                ("Goals & Non-Goals", ["goals", "目标", "non-goals", "非目标"]),
                ("Functional Requirements (EARS)", ["ears", "the system shall"]),
                ("ADR Candidates", ["adr", "decision", "why"]),
                ("Acceptance Criteria", ["given", "when", "then"]),
                ("Out of Scope", ["out of scope", "不做", "非目标"]),
            ],
        )
    if relative == "doc/detailed-design.md":
        return _validate_tokens(
            path,
            text,
            [
                ("module design", ["模块", "module"]),
                ("contracts", ["api", "契约", "接口", "contract"]),
                ("ADR", ["adr", "decision", "why"]),
                ("acceptance mapping", ["acceptance", "验收", "given", "when", "then"]),
                ("test strategy", ["test", "测试", "验证"]),
            ],
        )
    if relative == "doc/tasks/progress.md":
        issues = _validate_tokens(
            path,
            text,
            [
                ("module progress checklist", ["- [ ]", "- [x]"]),
                ("execution order or blockers", ["blocked", "阻塞", "顺序", "依赖"]),
            ],
        )
        return issues
    if relative.startswith("doc/tasks/") and path.name != "progress.md":
        return _validate_tokens(
            path,
            text,
            [
                ("task checklist", ["- [ ]", "- [x]"]),
                ("AFK/HITL marker", ["afk", "hitl"]),
                ("traceability", ["ears", "adr", "acceptance", "验收"]),
                ("test requirements", ["test", "测试", "验证"]),
                ("file scope", ["file", "文件"]),
            ],
        )
    if relative == "doc/prompt.md":
        issues = _validate_tokens(
            path,
            text,
            [
                ("progress tracking", ["doc/tasks/progress.md", "progress.md"]),
                ("verification", ["test", "验证", "测试"]),
                ("spec compliance", ["spec", "adr", "acceptance", "验收"]),
            ],
        )
        mentions_subagents = any(
            token in lowered for token in ["subagent", "sub agent", "子 agent", "子 agents"]
        )
        marks_optional = any(token in lowered for token in ["可选", "optional", "只有当", "不得强制"])
        if mentions_subagents and not marks_optional:
            issues.append(ArtifactValidationIssue(path, "subagents must be optional, not mandatory"))
        return issues
    return []


def _validate_tokens(
    path: Path,
    text: str,
    requirements: list[tuple[str, list[str]]],
) -> list[ArtifactValidationIssue]:
    lowered = text.lower()
    issues: list[ArtifactValidationIssue] = []
    for label, tokens in requirements:
        if not all(token.lower() in lowered for token in tokens[:1]) and not any(
            token.lower() in lowered for token in tokens
        ):
            issues.append(ArtifactValidationIssue(path, f"missing {label}"))
    return issues


def _relative(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
