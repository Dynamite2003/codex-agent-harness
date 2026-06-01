from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from .config import load_config
from .python_bootstrap import bootstrap_python_project
from .runner import create_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="codex-harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="copy the example harness config into a project")
    init_parser.add_argument("--path", default=".", help="project path")
    init_parser.add_argument("--force", action="store_true", help="overwrite existing harness.json")

    run_parser = subparsers.add_parser("run", help="create a phased harness run")
    run_parser.add_argument("--config", required=True, help="path to harness json config")
    run_parser.add_argument("--goal", required=True, help="raw user goal")
    run_parser.add_argument("--project-root", default=".", help="target project root")
    run_parser.add_argument("--execute", action="store_true", help="execute generated Codex CLI commands")

    bootstrap_parser = subparsers.add_parser("bootstrap-python", help="prepare a uv-based Python project")
    bootstrap_parser.add_argument("--path", default=".", help="target Python project path")
    bootstrap_parser.add_argument("--package-name", help="Python package directory name")
    bootstrap_parser.add_argument("--execute", action="store_true", help="run uv venv and install dev dependencies")

    args = parser.parse_args(argv)

    if args.command == "init":
        return _init(Path(args.path), force=args.force)
    if args.command == "run":
        return _run(args)
    if args.command == "bootstrap-python":
        return _bootstrap_python(args)

    parser.error(f"Unknown command: {args.command}")
    return 2


def _init(path: Path, *, force: bool) -> int:
    target = path.resolve() / "harness.json"
    if target.exists() and not force:
        print(f"Refusing to overwrite existing config: {target}", file=sys.stderr)
        return 1

    example = Path(__file__).resolve().parents[2] / "examples" / "basic.harness.json"
    if example.exists():
        shutil.copyfile(example, target)
    else:
        target.write_text(_fallback_config(), encoding="utf-8")

    print(f"Created {target}")
    return 0


def _run(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).resolve())
    project_root = Path(args.project_root).resolve()
    run = create_run(
        config=config,
        user_goal=args.goal,
        project_root=project_root,
        execute=args.execute,
    )
    print(f"Run created: {run.run_dir}")
    for phase in run.phases:
        print(f"- {phase.phase_id}: {phase.prompt_file}")
    if not args.execute:
        print("Dry run only. No project artifacts were generated. Re-run with --execute to call Codex CLI.")
    return 0


def _bootstrap_python(args: argparse.Namespace) -> int:
    result = bootstrap_python_project(
        project_root=Path(args.path).resolve(),
        package_name=args.package_name,
        execute=args.execute,
    )
    print(f"Python project prepared: {result.project_root}")
    print(f"- pyproject: {result.pyproject_path}")
    print(f"- bootstrap script: {result.script_path}")
    if result.executed:
        print("- executed: uv venv + dev dependency install")
    else:
        print("Dry run for commands. Re-run with --execute or run the bootstrap script.")
    return 0


def _fallback_config() -> str:
    return """{
  "project_name": "local-project",
  "workspace": ".harness",
  "codex": {"command": ["codex", "exec", "--sandbox", "workspace-write", "{prompt_stdin}"]},
  "isolation": {"new_conversation_per_phase": true, "artifact_only_context": true},
  "global_constraints": [],
  "prompt_style": {"language": "zh-CN", "tone": "direct", "must_include": ["目标", "输入", "输出", "步骤"]},
  "phases": [
    {"id": "requirements", "title": "需求", "goal": "明确用户需求：{user_goal}", "input": "当前项目目录：{project_root}", "output": "请在 doc/proposal.md 生成需求文档。", "steps": "只做需求澄清，不做设计或实现。", "expected_outputs": ["doc/proposal.md"]},
    {"id": "design", "title": "设计", "goal": "根据需求文档生成详细设计文档。", "input": "需求文档 doc/proposal.md。\\n当前解析到的需求文档：\\n{context_files}", "output": "设计文档 doc/detailed-design.md。", "steps": "根据需求文档的内容，划分出模块，识别模块之间的关系，生成详细设计文档。不要猜测我的意图，任何不明确的地方向我询问。", "context_inputs": ["doc/proposal.md"], "expected_outputs": ["doc/detailed-design.md"]},
    {"id": "tasks", "title": "任务", "goal": "为每一个模块划分最小可执行的任务。", "input": "需求文档：doc/proposal.md；设计文档：doc/detailed-design.md。\\n当前解析到的输入文档：\\n{context_files}", "output": "任务列表：\\n- doc/tasks/<module-name>.md（每一个模块对应一个）。\\n- doc/tasks/progress.md（总体进度）。", "steps": "根据需求文档和详细设计，为每一个模块生成 vibe coding 的最小任务。每一个模块对应一个 <module-name>.md，用 checklist 表示子任务是否完成。在 progress.md 中用 checklist 表示模块是否完成。", "context_inputs": ["doc/proposal.md", "doc/detailed-design.md"], "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"]},
    {"id": "implementation", "title": "实现", "goal": "生成 Vibe Coding 用的 prompt。", "input": "需求文档 doc/proposal.md；详细设计：doc/detailed-design.md；任务划分：doc/tasks。\\n当前解析到的输入：\\n{context_files}", "output": "doc/prompt.md。", "steps": "阅读输入信息，了解当前要实现的工程，生成 doc/prompt.md 用来作为 Vibe Coding 的起始 prompt。doc/prompt.md 必须指定主 agent 作为监督 Agent 跟踪整体进度，读取并维护 doc/tasks/progress.md。主 agent 根据 progress.md 自动拉起多个子 agents，每个子 agent 负责一个模块或一个明确的最小任务，避免单个 agent 上下文过长。代码必须有完整的 pytest 单元测试并通过 mypy 和 ruff 检查。生成 prompt 过程中任何不明确的地方需要向我提问。", "context_inputs": ["doc/proposal.md", "doc/detailed-design.md", "doc/tasks"], "expected_outputs": ["doc/prompt.md"]}
  ]
}
"""


if __name__ == "__main__":
    raise SystemExit(main())
