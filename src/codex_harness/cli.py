from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from .config import load_config
from .defaults import default_config_text
from .python_bootstrap import bootstrap_python_project
from .runner import (
    FORCE_NEXT_PHASE,
    SKIP_PHASE,
    STOP_RUN,
    PhaseCommandFailedError,
    PhaseNeedsUserInputError,
    PhaseOutputMissingError,
    PhaseRun,
    create_run,
)


def main(argv: list[str] | None = None) -> int:
    argv = _normalize_argv(argv)
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

    start_parser = subparsers.add_parser("start", help="run the default harness with fewer flags")
    start_parser.add_argument("goal", help="raw user goal")
    start_parser.add_argument("-C", "--project-root", default=".", help="target project root")
    start_parser.add_argument("--config", help="path to harness json config")
    start_parser.add_argument("--dry-run", action="store_true", help="only create harness prompts")

    bootstrap_parser = subparsers.add_parser("bootstrap-python", help="prepare a uv-based Python project")
    bootstrap_parser.add_argument("--path", default=".", help="target Python project path")
    bootstrap_parser.add_argument("--package-name", help="Python package directory name")
    bootstrap_parser.add_argument("--execute", action="store_true", help="run uv venv and install dev dependencies")

    clean_parser = subparsers.add_parser("clean-runs", help="remove old harness run directories")
    clean_parser.add_argument("-C", "--project-root", default=".", help="target project root")
    clean_parser.add_argument("--workspace", default=".harness", help="harness workspace directory")
    clean_parser.add_argument("--keep", type=int, default=10, help="number of newest runs to keep")
    clean_parser.add_argument("--dry-run", action="store_true", help="print runs that would be removed")

    args = parser.parse_args(argv)

    if args.command == "init":
        return _init(Path(args.path), force=args.force)
    if args.command == "run":
        return _run(args)
    if args.command == "start":
        return _start(args)
    if args.command == "bootstrap-python":
        return _bootstrap_python(args)
    if args.command == "clean-runs":
        return _clean_runs(args)

    parser.error(f"Unknown command: {args.command}")
    return 2


def _normalize_argv(argv: list[str] | None) -> list[str] | None:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        return argv
    known_commands = {"init", "run", "start", "bootstrap-python", "clean-runs", "-h", "--help"}
    if argv[0] in known_commands:
        return argv
    return ["start", *argv]


def _init(path: Path, *, force: bool) -> int:
    target = path.resolve() / "harness.json"
    if target.exists() and not force:
        print(f"Refusing to overwrite existing config: {target}", file=sys.stderr)
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(default_config_text(), encoding="utf-8")

    print(f"Created {target}")
    return 0


def _start(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    config_path = Path(args.config).resolve() if args.config else _default_config_path(project_root)
    run_args = argparse.Namespace(
        config=str(config_path),
        goal=args.goal,
        project_root=str(project_root),
        execute=not args.dry_run,
    )
    return _run(run_args)


def _default_config_path(project_root: Path) -> Path:
    project_config = project_root / "harness.json"
    if project_config.exists():
        return project_config
    fallback_config = project_root / ".harness" / "default.harness.json"
    if not fallback_config.exists():
        fallback_config.parent.mkdir(parents=True, exist_ok=True)
        fallback_config.write_text(default_config_text(), encoding="utf-8")
    return fallback_config


def _run(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config).resolve())
    project_root = Path(args.project_root).resolve()
    try:
        run = create_run(
            config=config,
            user_goal=args.goal,
            project_root=project_root,
            execute=args.execute,
            user_input_provider=_read_user_input if args.execute else None,
            output_missing_provider=_read_missing_output_instruction if args.execute else None,
        )
    except PhaseNeedsUserInputError as error:
        print(str(error), file=sys.stderr)
        return 1
    except PhaseOutputMissingError as error:
        print(str(error), file=sys.stderr)
        return 1
    except PhaseCommandFailedError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"Run created: {run.run_dir}")
    for phase in run.phases:
        print(f"- {phase.phase_id}: {phase.prompt_file}")
    if not args.execute:
        print("Dry run only. No project artifacts were generated. Re-run with --execute to call Codex CLI.")
    return 0


def _read_user_input(phase_run: PhaseRun, request: str) -> str:
    print(
        "\n"
        f"Phase '{phase_run.phase_id}' needs your input before continuing.\n"
        f"Questions were written to: {phase_run.needs_user_input_file}\n"
        "Questions:\n"
        f"{request.strip()}\n\n"
        "Enter your answer. Finish with a line containing only END.\n"
        "Enter NEXT_PHASE on its own line to record any typed answer and validate the current phase artifacts.",
        file=sys.stderr,
    )
    lines: list[str] = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            return ""
        marker = line.rstrip("\n")
        if marker == "NEXT_PHASE":
            answer = "".join(lines).strip()
            return FORCE_NEXT_PHASE + ("\n" + answer if answer else "")
        if marker == "END":
            return "".join(lines).strip()
        lines.append(line)


def _read_missing_output_instruction(phase_run: PhaseRun, missing: list[Path]) -> str:
    formatted = "\n".join(f"- {path}" for path in missing)
    print(
        "\n"
        f"Phase '{phase_run.phase_id}' did not create required artifacts.\n"
        f"Missing outputs:\n{formatted}\n\n"
        "Enter an instruction to rerun this phase, then finish with a line containing only END.\n"
        "Enter SKIP_PHASE on its own line to continue anyway.\n"
        "Enter STOP on its own line to stop.",
        file=sys.stderr,
    )
    lines: list[str] = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            return STOP_RUN
        marker = line.rstrip("\n")
        if marker == "SKIP_PHASE":
            return SKIP_PHASE
        if marker == "STOP":
            return STOP_RUN
        if marker == "END":
            return "".join(lines).strip()
        lines.append(line)


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


def _clean_runs(args: argparse.Namespace) -> int:
    keep = args.keep
    if keep < 0:
        print("--keep must be greater than or equal to 0", file=sys.stderr)
        return 2

    runs_dir = Path(args.project_root).resolve() / args.workspace / "runs"
    if not runs_dir.exists():
        print(f"No runs directory found: {runs_dir}")
        return 0

    runs = sorted((path for path in runs_dir.iterdir() if path.is_dir()), key=lambda path: path.name, reverse=True)
    to_remove = runs[keep:]
    for run_dir in to_remove:
        if args.dry_run:
            print(f"Would remove {run_dir}")
        else:
            shutil.rmtree(run_dir)
            print(f"Removed {run_dir}")

    action = "Would remove" if args.dry_run else "Removed"
    print(f"{action} {len(to_remove)} run(s); kept {len(runs) - len(to_remove)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
