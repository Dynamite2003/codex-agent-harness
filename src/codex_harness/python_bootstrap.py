from __future__ import annotations

import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

DEV_DEPENDENCIES = ["ruff", "mypy", "pytest", "pytest-cov"]


@dataclass(frozen=True)
class BootstrapResult:
    project_root: Path
    pyproject_path: Path
    script_path: Path
    commands: list[list[str]]
    executed: bool


def bootstrap_python_project(
    *,
    project_root: Path,
    package_name: str | None = None,
    execute: bool = False,
) -> BootstrapResult:
    project_root.mkdir(parents=True, exist_ok=True)
    package = package_name or _default_package_name(project_root)
    pyproject_path = project_root / "pyproject.toml"
    _ensure_pyproject(pyproject_path, project_root.name, package)

    commands = [
        ["uv", "venv"],
        ["uv", "add", "--dev", *DEV_DEPENDENCIES],
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "mypy", package],
        ["uv", "run", "pytest"],
    ]

    harness_dir = project_root / ".harness" / "bootstrap"
    harness_dir.mkdir(parents=True, exist_ok=True)
    script_path = harness_dir / "python-bootstrap.sh"
    _write_script(script_path, commands)

    if execute:
        if shutil.which("uv") is None:
            raise RuntimeError("uv is not installed or not on PATH. Install uv first, then re-run bootstrap-python --execute.")
        for command in commands[:2]:
            subprocess.run(command, cwd=project_root, check=True)

    return BootstrapResult(
        project_root=project_root,
        pyproject_path=pyproject_path,
        script_path=script_path,
        commands=commands,
        executed=execute,
    )


def _default_package_name(project_root: Path) -> str:
    return project_root.name.lower().replace("-", "_").replace(" ", "_")


def _ensure_pyproject(path: Path, project_name: str, package_name: str) -> None:
    if not path.exists():
        path.write_text(_new_pyproject(project_name, package_name), encoding="utf-8")
        package_dir = path.parent / package_name
        package_dir.mkdir(exist_ok=True)
        init_file = package_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Project package."""\n', encoding="utf-8")
        tests_dir = path.parent / "tests"
        tests_dir.mkdir(exist_ok=True)
        return

    content = path.read_text(encoding="utf-8")
    additions: list[str] = []
    if "[tool.ruff]" not in content:
        additions.append(_ruff_config())
    if "[tool.mypy]" not in content:
        additions.append(_mypy_config(package_name))
    if "[tool.pytest.ini_options]" not in content:
        additions.append(_pytest_config())
    if "[dependency-groups]" not in content and "[tool.uv]" not in content:
        additions.append(_dependency_groups())

    if additions:
        separator = "\n" if content.endswith("\n") else "\n\n"
        path.write_text(content + separator + "\n\n".join(additions).strip() + "\n", encoding="utf-8")


def _new_pyproject(project_name: str, package_name: str) -> str:
    return f"""[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["{package_name}*"]

{_dependency_groups()}

{_ruff_config()}

{_mypy_config(package_name)}

{_pytest_config()}
"""


def _dependency_groups() -> str:
    deps = ",\n  ".join(f'"{item}"' for item in DEV_DEPENDENCIES)
    return f"""[dependency-groups]
dev = [
  {deps}
]"""


def _ruff_config() -> str:
    return """[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = []"""


def _mypy_config(package_name: str) -> str:
    return f"""[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_configs = true
files = ["{package_name}", "tests"]"""


def _pytest_config() -> str:
    return '''[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"'''


def _write_script(path: Path, commands: list[list[str]]) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        'if ! command -v uv >/dev/null 2>&1; then',
        '  echo "uv is required. Install it first: https://docs.astral.sh/uv/getting-started/installation/" >&2',
        "  exit 1",
        "fi",
        "",
    ]
    lines.extend(shlex.join(command) for command in commands)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o755)
