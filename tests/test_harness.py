from __future__ import annotations

import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Any

from codex_harness.cli import main
from codex_harness.config import load_config, parse_config
from codex_harness.defaults import default_config_text
from codex_harness.python_bootstrap import bootstrap_python_project
from codex_harness.runner import (
    FORCE_NEXT_PHASE,
    SKIP_PHASE,
    PhaseArtifactInvalidError,
    PhaseCommandFailedError,
    PhaseNeedsUserInputError,
    PhaseOutputMissingError,
    PhaseRun,
    create_run,
)


class HarnessTests(unittest.TestCase):
    def test_start_uses_default_config_and_current_style_args(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = main(["start", "-C", str(root), "--dry-run", "Build a feature."])

            self.assertEqual(result, 0)
            runs_dir = root / ".harness" / "runs"
            run_dir = next(runs_dir.iterdir())
            self.assertTrue((run_dir / "requirements" / "prompt.md").exists())
            self.assertIn(
                "Build a feature.",
                (run_dir / "requirements" / "prompt.md").read_text(encoding="utf-8"),
            )

    def test_goal_without_subcommand_defaults_to_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = main(["-C", str(root), "--dry-run", "Build a feature."])

            self.assertEqual(result, 0)
            self.assertTrue((root / ".harness" / "runs").exists())

    def test_init_skill_flow_installs_skills_and_quickstart(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            codex_home = Path(tmp) / "codex-home"

            result = main(["init-skill-flow", "--path", str(root), "--codex-home", str(codex_home)])

            self.assertEqual(result, 0)
            self.assertTrue((codex_home / "skills" / "vibe2spec-flow" / "SKILL.md").exists())
            self.assertTrue((codex_home / "skills" / "expand-requirements-prompt" / "SKILL.md").exists())
            self.assertTrue((root / "doc" / "specs").is_dir())
            self.assertTrue((root / "doc" / "tasks").is_dir())
            quickstart = (root / "doc" / "vibe2spec-quickstart.md").read_text(encoding="utf-8")
            self.assertIn("$vibe2spec-flow", quickstart)

    def test_validate_artifacts_reports_missing_spec_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "doc"
            doc.mkdir()
            (doc / "proposal.md").write_text("# Proposal\n\n功能正常。\n", encoding="utf-8")

            result = main(["validate-artifacts", "-C", str(root)])

            self.assertEqual(result, 1)

    def test_validate_artifacts_reports_missing_quality_lens_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "doc"
            doc.mkdir()
            (doc / "proposal.md").write_text(
                "# Proposal\n\n"
                "## Context\nContext.\n\n"
                "## Goals & Non-Goals\n目标和非目标。\n\n"
                "## Functional Requirements (EARS)\nWHEN user acts THE SYSTEM SHALL respond.\n\n"
                "## ADR Candidates\nDecision: simple. Why: MVP.\n\n"
                "## Acceptance Criteria\nGIVEN state WHEN action THEN result.\n\n"
                "## Out of Scope\n不做支付。\n",
                encoding="utf-8",
            )

            result = main(["validate-artifacts", "-C", str(root)])

            self.assertEqual(result, 1)

    def test_validate_artifacts_accepts_spec_first_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_valid_artifacts(root)

            result = main(["validate-artifacts", "-C", str(root)])

            self.assertEqual(result, 0)

    def test_create_run_writes_phase_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["codex", "exec", "{prompt_stdin}"]},
                    "global_constraints": ["Keep scope small."],
                    "prompt_style": {"must_include": ["当前阶段目标"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Clarify {user_goal}.",
                            "input": "Project root: {project_root}",
                            "output": "Write doc/proposal.md.",
                            "steps": "Ask questions before assuming.",
                            "context_inputs": [],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design only.",
                            "input": "Context:\n{context_files}",
                            "output": "Write doc/detailed-design.md.",
                            "steps": "Read requirements first.",
                            "context_inputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Plan tasks only.",
                            "input": "Context:\n{context_files}",
                            "output": "Write doc/tasks/<module-name>.md and doc/tasks/progress.md.",
                            "steps": "Create ordered tasks.",
                            "context_inputs": ["doc/proposal.md", "doc/detailed-design.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Generate Vibe Coding prompt.",
                            "input": "Context:\n{context_files}",
                            "output": "Write doc/prompt.md.",
                            "steps": "Supervisor agent spawns subagents.",
                            "context_inputs": [
                                "doc/proposal.md",
                                "doc/detailed-design.md",
                                "doc/tasks",
                            ],
                        }
                    ],
                }
            )

            run = create_run(config=config, user_goal="Build a feature.", project_root=root)

            phase = run.phases[0]
            self.assertTrue(phase.prompt_file.exists())
            self.assertTrue(phase.context_file.exists())
            self.assertTrue(phase.command_file.exists())
            self.assertIn("Build a feature.", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertIn("目标：", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertIn("输入：", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertIn("输出：", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertIn("步骤：", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertIn("这是 Requirements 阶段的新对话", phase.prompt_file.read_text(encoding="utf-8"))
            self.assertTrue((run.run_dir / "requirements" / "conversation").exists())
            self.assertEqual(phase.command[-1], "-")
            self.assertTrue(phase.prompt_stdin)
            self.assertIn(f"< {phase.prompt_file}", phase.command_file.read_text(encoding="utf-8"))

    def test_run_id_is_unique_for_back_to_back_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = load_config(Path("examples/basic.harness.json"))

            first = create_run(config=config, user_goal="Goal", project_root=root)
            second = create_run(config=config, user_goal="Goal", project_root=root)

            self.assertNotEqual(first.run_id, second.run_id)
            self.assertTrue(first.run_dir.exists())
            self.assertTrue(second.run_dir.exists())

    def test_prompt_style_is_rendered_into_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["codex", "exec", "{prompt_file}"]},
                    "prompt_style": {
                        "language": "en-US",
                        "tone": "concise",
                        "must_include": ["Summary", "Risks"],
                    },
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Implement.",
                            "input": "Context.",
                            "output": "Write implementation.",
                            "steps": "Code.",
                        },
                    ],
                }
            )

            run = create_run(config=config, user_goal="Goal", project_root=root)
            prompt = run.phases[0].prompt_file.read_text(encoding="utf-8")

            self.assertIn("Prompt 风格：语言：en-US；语气：concise", prompt)
            self.assertIn("Summary、Risks", prompt)

    def test_context_inputs_are_declared_and_missing_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["codex", "exec", "{prompt_file}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context:\n{context_files}",
                            "output": "Write design.",
                            "steps": "Read.",
                            "context_inputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Implement.",
                            "input": "Context.",
                            "output": "Write implementation.",
                            "steps": "Code.",
                        }
                    ],
                }
            )

            run = create_run(config=config, user_goal="Goal", project_root=root)
            context = json.loads(run.phases[1].context_file.read_text(encoding="utf-8"))
            prompt = run.phases[1].prompt_file.read_text(encoding="utf-8")

            self.assertEqual(context["context_inputs"], ["doc/proposal.md"])
            self.assertEqual(context["missing_context_files"], ["doc/proposal.md"])
            self.assertEqual(context["conversation"]["mode"], "new_per_phase")
            self.assertIn("doc/proposal.md (missing)", prompt)

    def test_context_inputs_resolve_against_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc_dir = root / "doc"
            doc_dir.mkdir()
            (doc_dir / "proposal.md").write_text("# Proposal\n", encoding="utf-8")
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["codex", "exec", "{prompt_file}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context:\n{context_files}",
                            "output": "Write design.",
                            "steps": "Read.",
                            "context_inputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Implement.",
                            "input": "Context.",
                            "output": "Write implementation.",
                            "steps": "Code.",
                        },
                    ],
                }
            )

            run = create_run(config=config, user_goal="Goal", project_root=root)
            context = json.loads(run.phases[1].context_file.read_text(encoding="utf-8"))
            prompt = run.phases[1].prompt_file.read_text(encoding="utf-8")

            self.assertEqual(context["resolved_context_files"], [str(root / "doc" / "proposal.md")])
            self.assertEqual(context["missing_context_files"], [])
            self.assertIn("doc/proposal.md (exists)", prompt)

    def test_rejects_non_standard_phase_sequence(self) -> None:
        with self.assertRaises(ValueError):
            parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["codex", "exec", "{prompt_file}"]},
                    "phases": [
                        {
                            "id": "discover",
                            "title": "Discover",
                            "goal": "Goal.",
                            "input": "Input.",
                            "output": "Output.",
                            "steps": "Steps.",
                        }
                    ],
                }
            )

    def test_rejects_mistyped_nested_config_fields(self) -> None:
        base: dict[str, Any] = {
            "project_name": "test",
            "workspace": ".harness",
            "codex": {"command": ["codex", "exec", "{prompt_file}"]},
            "phases": [
                {
                    "id": "requirements",
                    "title": "Requirements",
                    "goal": "Requirements.",
                    "input": "None.",
                    "output": "Write docs.",
                    "steps": "Ask.",
                },
                {
                    "id": "design",
                    "title": "Design",
                    "goal": "Design.",
                    "input": "Context.",
                    "output": "Write design.",
                    "steps": "Read.",
                },
                {
                    "id": "tasks",
                    "title": "Tasks",
                    "goal": "Tasks.",
                    "input": "Context.",
                    "output": "Write tasks.",
                    "steps": "Split.",
                },
                {
                    "id": "implementation",
                    "title": "Implementation",
                    "goal": "Implement.",
                    "input": "Context.",
                    "output": "Write implementation.",
                    "steps": "Code.",
                },
            ],
        }

        invalid_bool = dict(base)
        invalid_bool["isolation"] = {"new_conversation_per_phase": "false"}
        with self.assertRaisesRegex(ValueError, "must be a boolean"):
            parse_config(invalid_bool)

        invalid_constraints = dict(base)
        invalid_constraints["global_constraints"] = "Keep scope small."
        with self.assertRaisesRegex(ValueError, "global_constraints must be a list of strings"):
            parse_config(invalid_constraints)

        invalid_context = dict(base)
        invalid_context["phases"] = [dict(item) for item in base["phases"]]
        invalid_context["phases"][1]["context_inputs"] = "doc/proposal.md"
        with self.assertRaisesRegex(ValueError, "context_inputs must be a list of strings"):
            parse_config(invalid_context)

    def test_default_tasks_prompt_uses_module_task_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = load_config(Path("examples/basic.harness.json"))

            run = create_run(config=config, user_goal="Build a Python project.", project_root=root)
            prompt = run.phases[2].prompt_file.read_text(encoding="utf-8")
            context = json.loads(run.phases[2].context_file.read_text(encoding="utf-8"))

            self.assertIn("为每一个模块划分最小可执行的任务", prompt)
            self.assertIn("需求文档：doc/proposal.md；设计文档：doc/detailed-design.md", prompt)
            self.assertIn("doc/tasks/<module-name>.md", prompt)
            self.assertIn("doc/tasks/progress.md", prompt)
            self.assertIn("用 checklist 表示子任务是否完成", prompt)
            self.assertIn("AFK/HITL", prompt)
            self.assertIn("每个任务必须能追溯到 EARS 需求、ADR 或 Acceptance Criteria", prompt)
            self.assertEqual(context["context_inputs"], ["doc/proposal.md", "doc/detailed-design.md"])

    def test_default_requirements_and_design_prompts_use_spec_first_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = load_config(Path("examples/basic.harness.json"))

            run = create_run(config=config, user_goal="Build a Python project.", project_root=root)
            requirements_prompt = run.phases[0].prompt_file.read_text(encoding="utf-8")
            design_prompt = run.phases[1].prompt_file.read_text(encoding="utf-8")

            self.assertIn("Spec-first 需求文档", requirements_prompt)
            self.assertIn("Functional Requirements (EARS)", requirements_prompt)
            self.assertIn("Key Decisions / ADR Candidates", requirements_prompt)
            self.assertIn("Acceptance Criteria (GIVEN-WHEN-THEN)", requirements_prompt)
            self.assertIn("doc/specs/index.md", requirements_prompt)
            self.assertIn("Key Design Decisions (ADR)", design_prompt)
            self.assertIn("需要回填的 spec 文件", design_prompt)

    def test_default_implementation_prompt_generates_lightweight_sequential_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = load_config(Path("examples/basic.harness.json"))

            run = create_run(config=config, user_goal="Build a Python project.", project_root=root)
            prompt = run.phases[3].prompt_file.read_text(encoding="utf-8")
            context = json.loads(run.phases[3].context_file.read_text(encoding="utf-8"))

            self.assertIn("生成 Vibe Coding 用的 prompt", prompt)
            self.assertIn("doc/prompt.md", prompt)
            self.assertIn("默认采用单 agent 顺序执行", prompt)
            self.assertIn("doc/tasks/progress.md", prompt)
            self.assertIn("不得强制并行或强制开启多个 subagents", prompt)
            self.assertIn("按项目技术栈补充 focused tests 或等价验证", prompt)
            self.assertIn("先识别现有技术栈和可用工具", prompt)
            self.assertIn("不要为静态 Web、无依赖项目或已有项目强行引入不存在的 uv", prompt)
            self.assertIn("静态 Web 或无依赖前端项目至少做契约测试", prompt)
            self.assertIn("遵守 Spec / ADR / Acceptance Criteria", prompt)
            self.assertIn("spec 回填或偏离记录", prompt)
            self.assertEqual(
                context["context_inputs"],
                ["doc/proposal.md", "doc/detailed-design.md", "doc/tasks"],
            )

    def test_execute_validates_real_phase_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path; "
                "root=Path('{project_root}'); "
                "doc=root/'doc'; "
                "tasks=doc/'tasks'; "
                "tasks.mkdir(parents=True, exist_ok=True); "
                "(doc/'proposal.md').write_text('# Proposal\\n\\n## Context\\nWhy.\\n\\n## Goals & Non-Goals\\n目标和非目标。\\n\\n## Target Users\\n目标用户。\\n\\n## Product Archetype / Success Mode / Domain Lenses\\nProduct Archetype: API/SDK/CLI. Success Mode: Correctness. Domain Lenses: Interface.\\n\\n## Failure Mode Lens\\nFailure Mode: 结果错误。\\n\\n## Functional Requirements (EARS)\\nWHEN user acts THE SYSTEM SHALL respond.\\n\\n## Behavioral Requirements\\n行为需求。\\n\\n## Quality Requirements\\n质量需求。\\n\\n## ADR Candidates\\nDecision: simple. Why: MVP.\\n\\n## Acceptance Criteria\\nGIVEN state WHEN action THEN result.\\n\\n## Out of Scope\\n不做支付。\\n\\n## Verification Strategy\\n验证策略。\\n\\n## Risks\\n风险。\\n', encoding='utf-8'); "
                "(doc/'detailed-design.md').write_text('# Design\\n\\n## 模块\\nmodule core.\\n\\n## API 契约\\napi contract.\\n\\n## Success Mode / Failure Mode Response\\nSuccess Mode: Correctness. Failure Mode: 结果错误。\\n\\n## Behavioral / Quality Design\\nBehavioral handling and Quality checks.\\n\\n## ADR\\nDecision: simple. Why: MVP.\\n\\n## Acceptance Mapping\\nGIVEN state WHEN action THEN result.\\n\\n## Test Strategy\\n测试验证。\\n', encoding='utf-8'); "
                "(tasks/'core.md').write_text('# Core Tasks\\n\\n## Checklist\\n- [x] 实现 core\\n\\n## Traceability\\nEARS / ADR / Acceptance.\\n\\n## AFK/HITL\\nAFK. HITL: none.\\n\\n## Test Requirements\\n测试验证。\\n\\n## File Scope\\n文件 src/core.py。\\n\\n## Success Mode / Failure Mode / Quality Trace\\nSuccess Mode: Correctness. Failure Mode: 结果错误。 Quality: tested.\\n', encoding='utf-8'); "
                "(tasks/'progress.md').write_text('# Progress\\n\\n## 顺序和阻塞\\nBlocked: none.\\n\\n- [x] core\\n', encoding='utf-8'); "
                "(doc/'prompt.md').write_text('# Prompt\\n\\nRead doc/tasks/progress.md. Follow Spec ADR Acceptance. Run test 验证. Check Success Mode, Failure Mode, and Quality Requirements.\\n', encoding='utf-8')"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write Spec-first docs with Functional Requirements (EARS), Key Decisions / ADR, and Acceptance Criteria.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "context_inputs": ["doc/proposal.md"],
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "context_inputs": ["doc/proposal.md", "doc/detailed-design.md"],
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "context_inputs": ["doc/proposal.md", "doc/detailed-design.md", "doc/tasks"],
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(config=config, user_goal="Goal", project_root=root, execute=True)
            status = json.loads((run.run_dir / "implementation" / "status.json").read_text())

            self.assertTrue((root / "doc" / "proposal.md").exists())
            self.assertTrue((root / "doc" / "detailed-design.md").exists())
            self.assertTrue((root / "doc" / "tasks" / "progress.md").exists())
            self.assertTrue((root / "doc" / "prompt.md").exists())
            self.assertTrue(status["ok"])
            self.assertEqual(status["missing_outputs"], [])
            self.assertFalse(status["artifact_invalid"])

    def test_execute_stops_when_artifact_content_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path; "
                "root=Path('{project_root}'); "
                "doc=root/'doc'; "
                "doc.mkdir(parents=True, exist_ok=True); "
                "(doc/'proposal.md').write_text('proposal only\\n', encoding='utf-8')"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write Spec-first docs with Functional Requirements (EARS), Key Decisions / ADR, and Acceptance Criteria.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                        },
                    ],
                }
            )

            with self.assertRaises(PhaseArtifactInvalidError):
                create_run(config=config, user_goal="Goal", project_root=root, execute=True)

            run_dir = next((root / ".harness" / "runs").iterdir())
            status = json.loads((run_dir / "requirements" / "status.json").read_text())
            self.assertTrue(status["artifact_invalid"])
            self.assertGreater(len(status["validation_issues"]), 0)

    def test_execute_stops_when_phase_requests_user_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path; "
                "import sys; "
                "phase=sys.argv[1]; "
                "root=Path('{project_root}'); "
                "doc=root/'doc'; "
                "doc.mkdir(exist_ok=True); "
                "\nif phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('draft\\n', encoding='utf-8')\n"
                "    print('HARNESS_NEEDS_USER_INPUT\\n1. 请确认目标平台。')\n"
                "else:\n"
                "    (doc/(phase + '.md')).write_text('should not run\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                        },
                    ],
                }
            )

            with self.assertRaises(PhaseNeedsUserInputError) as raised:
                create_run(config=config, user_goal="Goal", project_root=root, execute=True)

            self.assertIn("requested user input", str(raised.exception))
            run_dir = next((root / ".harness" / "runs").iterdir())
            phase_dir = run_dir / "requirements"
            status = json.loads((phase_dir / "status.json").read_text(encoding="utf-8"))

            self.assertTrue((phase_dir / "stdout.txt").exists())
            self.assertTrue((phase_dir / "needs-user-input.md").exists())
            self.assertTrue(status["needs_user_input"])
            self.assertFalse((root / "doc" / "detailed-design.md").exists())

    def test_execute_ignores_inline_marker_and_question_words_in_logs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal\\n', encoding='utf-8')\n"
                "    print('日志说明：prompt 中提到 HARNESS_NEEDS_USER_INPUT 只是协议文本，请确认不应暂停。')\n"
                "elif phase == 'design':\n"
                "    (doc/'detailed-design.md').write_text('design\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(config=config, user_goal="Goal", project_root=root, execute=True)
            requirements_dir = run.run_dir / "requirements"
            status = json.loads((requirements_dir / "status.json").read_text(encoding="utf-8"))

            self.assertTrue(status["ok"])
            self.assertFalse(status["needs_user_input"])
            self.assertFalse((requirements_dir / "needs-user-input.md").exists())
            self.assertTrue((root / "doc" / "prompt.md").exists())

    def test_execute_reads_user_input_and_resumes_same_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "prompt=sys.stdin.read()\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements' and '目标平台是 iOS' not in prompt:\n"
                "    print('HARNESS_NEEDS_USER_INPUT\\n1. 请确认目标平台。')\n"
                "elif phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal with iOS\\n', encoding='utf-8')\n"
                "elif phase == 'design':\n"
                "    (doc/'detailed-design.md').write_text('design\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'core.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}", "{prompt_stdin}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )
            requests: list[str] = []

            def answer(phase_run: PhaseRun, request: str) -> str:
                requests.append(phase_run.phase_id + ":" + request)
                return "目标平台是 iOS"

            run = create_run(config=config, user_goal="Goal", project_root=root, execute=True, user_input_provider=answer)
            requirements_dir = run.run_dir / "requirements"
            status = json.loads((requirements_dir / "status.json").read_text(encoding="utf-8"))

            self.assertEqual(len(requests), 1)
            self.assertIn("requirements:HARNESS_NEEDS_USER_INPUT", requests[0])
            self.assertFalse((requirements_dir / "needs-user-input.md").exists())
            self.assertIn("目标平台是 iOS", (requirements_dir / "user-answers.md").read_text(encoding="utf-8"))
            self.assertIn("目标平台是 iOS", run.phases[0].prompt_file.read_text(encoding="utf-8"))
            self.assertTrue(status["ok"])
            self.assertFalse(status["needs_user_input"])
            self.assertTrue((root / "doc" / "prompt.md").exists())

    def test_execute_can_force_next_phase_after_repeated_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal draft\\n', encoding='utf-8')\n"
                "    print('HARNESS_NEEDS_USER_INPUT\\n1. 还要继续确认吗？')\n"
                "elif phase == 'design':\n"
                "    (doc/'detailed-design.md').write_text('design\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'core.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(
                config=config,
                user_goal="Goal",
                project_root=root,
                execute=True,
                user_input_provider=lambda _phase_run, _request: FORCE_NEXT_PHASE,
            )
            requirements_dir = run.run_dir / "requirements"
            status = json.loads((requirements_dir / "status.json").read_text(encoding="utf-8"))

            self.assertTrue(status["ok"])
            self.assertFalse(status["needs_user_input"])
            self.assertTrue((requirements_dir / "force-next-phase.md").exists())
            self.assertFalse((requirements_dir / "needs-user-input.md").exists())
            self.assertTrue((root / "doc" / "prompt.md").exists())

    def test_force_next_phase_preserves_typed_answer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal draft\\n', encoding='utf-8')\n"
                "    print('HARNESS_NEEDS_USER_INPUT\\n1. 请确认。')\n"
                "elif phase == 'design':\n"
                "    (doc/'detailed-design.md').write_text('design\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(
                config=config,
                user_goal="Goal",
                project_root=root,
                execute=True,
                user_input_provider=lambda _phase_run, _request: FORCE_NEXT_PHASE + "\n用户已经回答的内容",
            )
            requirements_dir = run.run_dir / "requirements"

            self.assertIn("用户已经回答的内容", (requirements_dir / "user-answers.md").read_text(encoding="utf-8"))
            self.assertIn(
                "用户已经回答的内容",
                (requirements_dir / "force-next-phase.md").read_text(encoding="utf-8"),
            )

    def test_missing_outputs_can_be_retried_interactively(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "prompt=sys.stdin.read()\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal\\n', encoding='utf-8')\n"
                "elif phase == 'design' and '请补齐详细设计文档' in prompt:\n"
                "    (doc/'detailed-design.md').write_text('design\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}", "{prompt_stdin}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(
                config=config,
                user_goal="Goal",
                project_root=root,
                execute=True,
                output_missing_provider=lambda _phase_run, _missing: "请补齐详细设计文档",
            )

            self.assertTrue((root / "doc" / "detailed-design.md").exists())
            self.assertTrue((run.run_dir / "design" / "missing-output-retries.md").exists())

    def test_missing_outputs_can_be_stopped_without_traceback_error_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", "print('done')"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {"id": "design", "title": "Design", "goal": "Design.", "input": "Context.", "output": "Write design.", "steps": "Read."},
                        {"id": "tasks", "title": "Tasks", "goal": "Tasks.", "input": "Context.", "output": "Write tasks.", "steps": "Split."},
                        {"id": "implementation", "title": "Implementation", "goal": "Prompt.", "input": "Context.", "output": "Write prompt.", "steps": "Generate."},
                    ],
                }
            )

            with self.assertRaises(PhaseOutputMissingError):
                create_run(config=config, user_goal="Goal", project_root=root, execute=True)

    def test_command_failure_writes_status_without_subprocess_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", "import sys; sys.exit(7)"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                        },
                    ],
                }
            )

            with self.assertRaises(PhaseCommandFailedError) as raised:
                create_run(config=config, user_goal="Goal", project_root=root, execute=True)

            self.assertIn("exit code 7", str(raised.exception))
            run_dir = next((root / ".harness" / "runs").iterdir())
            status = json.loads((run_dir / "requirements" / "status.json").read_text(encoding="utf-8"))

            self.assertTrue((run_dir / "manifest.json").exists())
            self.assertTrue(status["command_failed"])
            self.assertEqual(status["returncode"], 7)

    def test_missing_outputs_can_be_skipped_with_audit_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = (
                "from pathlib import Path\n"
                "import sys\n"
                "phase=sys.argv[1]\n"
                "root=Path('{project_root}')\n"
                "doc=root/'doc'\n"
                "doc.mkdir(exist_ok=True)\n"
                "if phase == 'requirements':\n"
                "    (doc/'proposal.md').write_text('proposal\\n', encoding='utf-8')\n"
                "elif phase == 'tasks':\n"
                "    tasks=doc/'tasks'\n"
                "    tasks.mkdir(exist_ok=True)\n"
                "    (tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8')\n"
                "elif phase == 'implementation':\n"
                "    (doc/'prompt.md').write_text('prompt\\n', encoding='utf-8')\n"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", fake_codex, "{phase_id}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Requirements.",
                            "input": "None.",
                            "output": "Write docs.",
                            "steps": "Ask.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                            "expected_outputs": ["doc/detailed-design.md"],
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                            "expected_outputs": ["doc/tasks", "doc/tasks/progress.md"],
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Prompt.",
                            "input": "Context.",
                            "output": "Write prompt.",
                            "steps": "Generate.",
                            "expected_outputs": ["doc/prompt.md"],
                        },
                    ],
                }
            )

            run = create_run(
                config=config,
                user_goal="Goal",
                project_root=root,
                execute=True,
                output_missing_provider=lambda _phase_run, _missing: SKIP_PHASE,
            )
            design_status = json.loads((run.run_dir / "design" / "status.json").read_text(encoding="utf-8"))

            self.assertTrue(design_status["skipped"])
            self.assertTrue((run.run_dir / "design" / "skip-phase.md").exists())
            self.assertTrue((root / "doc" / "prompt.md").exists())

    def test_python_bootstrap_writes_uv_tooling_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sample-python"

            result = bootstrap_python_project(project_root=root, execute=False)
            content = result.pyproject_path.read_text(encoding="utf-8")
            parsed = tomllib.loads(content)

            self.assertTrue(result.script_path.exists())
            self.assertIn("project", parsed)
            self.assertIn("[dependency-groups]", content)
            self.assertIn('"ruff"', content)
            self.assertIn('"mypy"', content)
            self.assertIn('"pytest"', content)
            self.assertIn("[tool.ruff]", content)
            self.assertIn("[tool.mypy]", content)
            self.assertIn("[tool.pytest.ini_options]", content)

    def test_packaged_default_config_matches_example_config(self) -> None:
        packaged = json.loads(default_config_text())
        example = json.loads(Path("examples/basic.harness.json").read_text(encoding="utf-8"))

        self.assertEqual(packaged, example)

    def test_clean_runs_removes_old_run_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs_dir = root / ".harness" / "runs"
            old_run = runs_dir / "20240101T000000000000Z"
            new_run = runs_dir / "20240102T000000000000Z"
            old_run.mkdir(parents=True)
            new_run.mkdir(parents=True)

            result = main(["clean-runs", "-C", str(root), "--keep", "1"])

            self.assertEqual(result, 0)
            self.assertFalse(old_run.exists())
            self.assertTrue(new_run.exists())

    def test_clean_runs_dry_run_keeps_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs_dir = root / ".harness" / "runs"
            old_run = runs_dir / "20240101T000000000000Z"
            new_run = runs_dir / "20240102T000000000000Z"
            old_run.mkdir(parents=True)
            new_run.mkdir(parents=True)

            result = main(["clean-runs", "-C", str(root), "--keep", "1", "--dry-run"])

            self.assertEqual(result, 0)
            self.assertTrue(old_run.exists())
            self.assertTrue(new_run.exists())

    def test_execute_passes_prompt_to_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            writer = (
                "import pathlib, sys; "
                "phase=sys.argv[1]; "
                "root=pathlib.Path('{project_root}'); "
                "doc=root/'doc'; "
                "doc.mkdir(exist_ok=True); "
                "target=doc/'proposal.md' if phase == 'requirements' else doc/(phase + '.txt'); "
                "target.write_text(sys.stdin.read() + '\\n## Context\\nContext.\\n\\n## Goals & Non-Goals\\n目标和非目标。\\n\\n## Functional Requirements (EARS)\\nWHEN user acts THE SYSTEM SHALL respond.\\n\\n## ADR Candidates\\nDecision: simple. Why: MVP.\\n\\n## Acceptance Criteria\\nGIVEN state WHEN action THEN result.\\n\\n## Out of Scope\\n不做支付。\\n', encoding='utf-8')"
            )
            config = parse_config(
                {
                    "project_name": "test",
                    "workspace": ".harness",
                    "codex": {"command": ["python3", "-c", writer, "{phase_id}", "{prompt_stdin}"]},
                    "phases": [
                        {
                            "id": "requirements",
                            "title": "Requirements",
                            "goal": "Need {user_goal}.",
                            "input": "None.",
                            "output": "Write proposal.",
                            "steps": "Write.",
                            "expected_outputs": ["doc/proposal.md"],
                        },
                        {
                            "id": "design",
                            "title": "Design",
                            "goal": "Design.",
                            "input": "Context.",
                            "output": "Write design.",
                            "steps": "Read.",
                        },
                        {
                            "id": "tasks",
                            "title": "Tasks",
                            "goal": "Tasks.",
                            "input": "Context.",
                            "output": "Write tasks.",
                            "steps": "Split.",
                        },
                        {
                            "id": "implementation",
                            "title": "Implementation",
                            "goal": "Implement.",
                            "input": "Context.",
                            "output": "Write implementation.",
                            "steps": "Code.",
                        },
                    ],
                }
            )

            run = create_run(config=config, user_goal="Stdin feature", project_root=root, execute=True)

            proposal = (root / "doc" / "proposal.md").read_text(encoding="utf-8")
            self.assertIn("Need Stdin feature.", proposal)
            self.assertTrue(run.phases[0].prompt_stdin)


def _write_valid_artifacts(root: Path) -> None:
    doc = root / "doc"
    tasks = doc / "tasks"
    tasks.mkdir(parents=True)
    (doc / "proposal.md").write_text(
        "# Proposal\n\n"
        "## Context\nContext.\n\n"
        "## Goals & Non-Goals\n目标和非目标。\n\n"
        "## Target Users\n目标用户。\n\n"
        "## Product Archetype / Success Mode / Domain Lenses\n"
        "Product Archetype: API/SDK/CLI. Success Mode: Correctness. Domain Lenses: Interface.\n\n"
        "## Failure Mode Lens\nFailure Mode: 结果错误。\n\n"
        "## Functional Requirements (EARS)\nWHEN user acts THE SYSTEM SHALL respond.\n\n"
        "## Behavioral Requirements\n行为需求覆盖正常和失败状态。\n\n"
        "## Quality Requirements\n质量需求覆盖正确性和可维护性。\n\n"
        "## ADR Candidates\nDecision: simple. Why: MVP.\n\n"
        "## Acceptance Criteria\nGIVEN state WHEN action THEN result.\n\n"
        "## Out of Scope\n不做支付。\n\n"
        "## Verification Strategy\n验证策略包含单元测试。\n\n"
        "## Risks\n风险是需求遗漏。\n",
        encoding="utf-8",
    )
    (doc / "detailed-design.md").write_text(
        "# Design\n\n"
        "## 模块\nmodule core.\n\n"
        "## API 契约\napi contract.\n\n"
        "## Success Mode / Failure Mode Response\n"
        "Success Mode: Correctness. Failure Mode: 结果错误。\n\n"
        "## Behavioral / Quality Design\nBehavioral flow and Quality guard.\n\n"
        "## ADR\nDecision: simple. Why: MVP.\n\n"
        "## Acceptance Mapping\nGIVEN state WHEN action THEN result.\n\n"
        "## Test Strategy\n测试验证。\n",
        encoding="utf-8",
    )
    (tasks / "progress.md").write_text(
        "# Progress\n\n## 顺序和阻塞\nBlocked: none.\n\n- [x] core\n",
        encoding="utf-8",
    )
    (tasks / "core.md").write_text(
        "# Core Tasks\n\n"
        "## Checklist\n- [x] 实现 core\n\n"
        "## Traceability\nEARS / ADR / Acceptance.\n\n"
        "## AFK/HITL\nAFK. HITL: none.\n\n"
        "## Test Requirements\n测试验证。\n\n"
        "## File Scope\n文件 src/core.py。\n\n"
        "## Success Mode / Failure Mode / Quality Trace\n"
        "Success Mode: Correctness. Failure Mode: 结果错误。 Quality: tested.\n",
        encoding="utf-8",
    )
    (doc / "prompt.md").write_text(
        "# Prompt\n\n"
        "Read doc/tasks/progress.md. Follow Spec ADR Acceptance. Run test 验证. "
        "Check Success Mode, Failure Mode, and Quality Requirements.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
