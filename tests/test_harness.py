from __future__ import annotations

import json
import tempfile
import tomllib
import unittest
from pathlib import Path

from codex_harness.config import load_config, parse_config
from codex_harness.python_bootstrap import bootstrap_python_project
from codex_harness.runner import create_run


class HarnessTests(unittest.TestCase):
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
            self.assertEqual(context["context_inputs"], ["doc/proposal.md", "doc/detailed-design.md"])

    def test_default_implementation_prompt_generates_supervisor_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = load_config(Path("examples/basic.harness.json"))

            run = create_run(config=config, user_goal="Build a Python project.", project_root=root)
            prompt = run.phases[3].prompt_file.read_text(encoding="utf-8")
            context = json.loads(run.phases[3].context_file.read_text(encoding="utf-8"))

            self.assertIn("生成 Vibe Coding 用的 prompt", prompt)
            self.assertIn("doc/prompt.md", prompt)
            self.assertIn("监督 Agent 跟踪整体进度", prompt)
            self.assertIn("doc/tasks/progress.md", prompt)
            self.assertIn("自动拉起多个子 agents", prompt)
            self.assertIn("pytest 单元测试", prompt)
            self.assertIn("mypy 和 ruff 检查", prompt)
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
                "(doc/'proposal.md').write_text('proposal\\n', encoding='utf-8'); "
                "(doc/'detailed-design.md').write_text('design\\n', encoding='utf-8'); "
                "(tasks/'core.md').write_text('- [x] core\\n', encoding='utf-8'); "
                "(tasks/'progress.md').write_text('- [x] core\\n', encoding='utf-8'); "
                "(doc/'prompt.md').write_text('supervisor prompt\\n', encoding='utf-8')"
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
                "target.write_text(sys.stdin.read(), encoding='utf-8')"
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


if __name__ == "__main__":
    unittest.main()
