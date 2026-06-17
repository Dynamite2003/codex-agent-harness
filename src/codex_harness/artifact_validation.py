from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactValidationIssue:
    path: Path
    message: str


TokenGroup = list[str]
Requirement = tuple[str, list[TokenGroup]]

PROPOSAL_REQUIREMENTS: list[Requirement] = [
    ("Context", [["context", "背景"]]),
    ("Goals & Non-Goals", [["goals", "目标"], ["non-goals", "非目标"]]),
    ("Target Users", [["target users", "目标用户", "用户"]]),
    (
        "Product Archetype / Success Mode / Domain Lenses",
        [
            ["product archetype", "产品形态"],
            ["success mode", "成功模式"],
            ["domain lenses", "domain lens", "领域视角"],
        ],
    ),
    ("Failure Mode Lens", [["failure mode", "failure modes", "失败模式"]]),
    (
        "Functional Requirements (EARS)",
        [["functional requirements", "功能需求"], ["ears", "the system shall"]],
    ),
    ("Behavioral Requirements", [["behavioral requirements", "行为需求"]]),
    ("Quality Requirements", [["quality requirements", "质量需求"]]),
    ("ADR Candidates", [["adr"], ["decision", "决策"], ["why", "原因", "理由"]]),
    (
        "Acceptance Criteria",
        [["acceptance criteria", "验收标准"], ["given"], ["when"], ["then"]],
    ),
    ("Out of Scope", [["out of scope", "不做", "非目标"]]),
    ("Verification Strategy", [["verification strategy", "验证策略", "测试策略"]]),
    ("Risks", [["risks", "风险"]]),
]

DESIGN_REQUIREMENTS: list[Requirement] = [
    ("module design", [["模块", "module"]]),
    ("contracts", [["api", "契约", "接口", "contract"]]),
    ("domain/failure response", [["success mode", "成功模式"], ["failure mode", "失败模式"]]),
    ("behavioral/quality design", [["behavioral", "行为"], ["quality", "质量"]]),
    ("ADR", [["adr"], ["decision", "决策"], ["why", "原因", "理由"]]),
    ("acceptance mapping", [["acceptance", "验收"], ["given"], ["when"], ["then"]]),
    ("test strategy", [["test", "测试", "验证"]]),
]

PROGRESS_REQUIREMENTS: list[Requirement] = [
    ("module progress checklist", [["- [ ]", "- [x]"]]),
    ("execution order or blockers", [["blocked", "阻塞", "顺序", "依赖"]]),
]

TASK_REQUIREMENTS: list[Requirement] = [
    ("task checklist", [["- [ ]", "- [x]"]]),
    ("AFK/HITL marker", [["afk"], ["hitl"]]),
    ("traceability", [["ears", "adr", "acceptance", "验收"]]),
    ("test requirements", [["test", "测试", "验证"]]),
    ("file scope", [["file", "文件"]]),
    (
        "success/failure/quality trace",
        [["success mode", "成功模式"], ["failure mode", "失败模式"], ["quality", "质量"]],
    ),
]

PROMPT_REQUIREMENTS: list[Requirement] = [
    ("progress tracking", [["doc/tasks/progress.md", "progress.md"]]),
    ("verification", [["test", "验证", "测试"]]),
    ("spec compliance", [["spec"], ["adr"], ["acceptance", "验收"]]),
    (
        "quality and failure verification",
        [
            ["success mode", "成功模式"],
            ["failure mode", "失败模式"],
            ["quality requirements", "质量需求"],
        ],
    ),
]


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
        return _validate_requirements(path, text, PROPOSAL_REQUIREMENTS)
    if relative == "doc/detailed-design.md":
        return _validate_requirements(path, text, DESIGN_REQUIREMENTS)
    if relative == "doc/tasks/progress.md":
        return _validate_requirements(path, text, PROGRESS_REQUIREMENTS)
    if relative.startswith("doc/tasks/") and path.name != "progress.md":
        return _validate_requirements(path, text, TASK_REQUIREMENTS)
    if relative == "doc/prompt.md":
        issues = _validate_requirements(path, text, PROMPT_REQUIREMENTS)
        mentions_subagents = any(
            token in lowered for token in ["subagent", "sub agent", "子 agent", "子 agents"]
        )
        marks_optional = any(token in lowered for token in ["可选", "optional", "只有当", "不得强制"])
        if mentions_subagents and not marks_optional:
            issues.append(ArtifactValidationIssue(path, "subagents must be optional, not mandatory"))
        return issues
    return []


def _validate_requirements(
    path: Path,
    text: str,
    requirements: list[Requirement],
) -> list[ArtifactValidationIssue]:
    lowered = text.lower()
    issues: list[ArtifactValidationIssue] = []
    for label, token_groups in requirements:
        if not _matches_all_groups(lowered, token_groups):
            issues.append(ArtifactValidationIssue(path, f"missing {label}"))
    return issues


def _matches_all_groups(lowered_text: str, token_groups: list[TokenGroup]) -> bool:
    # Each group represents alternatives for one required concept.
    return all(any(token.lower() in lowered_text for token in group) for group in token_groups)


def _relative(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
