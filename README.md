# Codex Agent Harness

一个轻量的 Codex CLI harness，用来把软件开发任务拆成阶段执行，并把阶段上下文、prompt 和命令脚本落盘。

当前框架提供：

- 固定四阶段开发：每个具体需求都会拆成 `需求 -> 设计 -> 任务 -> 实现`。
- 四段式阶段 prompt：每个阶段发给 Codex 的 prompt 都只有 `目标`、`输入`、`输出`、`步骤` 四个部分。
- 隔离上下文：每个阶段默认开启新的 Codex 对话，只接收用户目标、全局约束，以及配置中声明的上游 artifacts。
- 自动润色 prompt：把原始目标整理成可直接交给 Codex CLI 的阶段化结构化 prompt。
- Python 项目启动协议：先用 `uv` 隔离环境，并配置 `ruff`、`mypy`、`pytest`。

## 快速开始

```bash
uv venv
uv sync --dev
uv run codex-harness run --config examples/basic.harness.json --goal "给现有 Web 项目增加登录页"
```

默认是 dry-run，只生成 harness 审计文件，不调用 Codex CLI，也不会生成 `doc/` 下的阶段产物。生成内容位于：

```text
.harness/runs/<run-id>/
```

每个阶段目录里会有：

- `prompt.md`：传给 Codex 的阶段 prompt。
- `context.json`：本阶段允许使用的上下文清单。
- `command.sh`：根据配置生成的 Codex CLI 命令。
- `stdout.txt` / `stderr.txt`：执行模式下保存 Codex CLI 输出。
- `needs-user-input.md`：如果 Codex 在当前阶段要求用户补充信息，harness 会写入问题并停止后续阶段。
- `conversation/`：当前阶段独立对话的预留目录，用来避免阶段间共享聊天上下文。

默认阶段为：

- `requirements`：生成需求文档 `doc/proposal.md`。
- `design`：基于需求生成详细设计文档 `doc/detailed-design.md`。
- `tasks`：基于需求和详细设计生成模块任务文件 `doc/tasks/<module-name>.md`，并维护总体进度 `doc/tasks/progress.md`。
- `implementation`：生成监督 Agent 使用的 Vibe Coding 起始 prompt `doc/prompt.md`，由监督 Agent 根据 `doc/tasks/progress.md` 自动拉起子 agents 完成实现和验证。

确认 prompt 后再执行：

```bash
uv run codex-harness run --config examples/basic.harness.json --goal "..." --execute
```

执行模式会真实调用 Codex CLI，并按阶段检查目标项目中的产物：

- `requirements` 必须生成 `doc/proposal.md`。
- `design` 必须生成 `doc/detailed-design.md`。
- `tasks` 必须生成 `doc/tasks/` 和 `doc/tasks/progress.md`。
- `implementation` 必须生成 `doc/prompt.md`。

如果某个阶段完成后缺少声明的产物，harness 会失败并在该阶段目录写入 `status.json`。

如果 Codex 在某个阶段输出 `HARNESS_NEEDS_USER_INPUT` 或明确要求用户确认/补充信息，执行模式会在同一个进程中暂停当前阶段，打印问题并等待你输入回答。输入多行回答后，用单独一行 `END` 提交；harness 会把回答记录到 `user-answers.md`，追加到当前阶段 `prompt.md`，重新执行同一阶段。只有当前阶段不再请求补充且产物校验通过后，才会进入下一阶段。如果 stdin 已关闭或回答为空，harness 会停止，并在该阶段目录写入 `needs-user-input.md` 和 `status.json`。

本地未安装包时也可以直接运行：

```bash
PYTHONPATH=src python3 -m codex_harness.cli run --config examples/basic.harness.json --goal "..."
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Python 项目启动

开启一个以 Python 为主要语言的新项目时，先运行：

```bash
codex-harness bootstrap-python --path /path/to/project
```

这会生成或补齐 `pyproject.toml`，写入 `ruff`、`mypy`、`pytest` 配置，并生成 `.harness/bootstrap/python-bootstrap.sh`。确认后执行：

```bash
codex-harness bootstrap-python --path /path/to/project --execute
```

执行模式要求本机已有 `uv`，并会运行：

```bash
uv venv
uv add --dev ruff mypy pytest pytest-cov
```

## 配置

参考 [examples/basic.harness.json](examples/basic.harness.json)。重点字段：

- `codex.command`：Codex CLI 命令模板。支持 `{prompt_file}`、`{prompt_stdin}`、`{phase_id}`、`{run_dir}`、`{project_root}`。当前 Codex CLI 推荐使用 `{prompt_stdin}`，harness 会把它渲染为 `-` 并通过 stdin 传入阶段 prompt；默认命令带 `--skip-git-repo-check`，允许在未初始化 git 或未信任目录中执行。
- `isolation.new_conversation_per_phase`：默认为 `true`，每个阶段都作为新的 Codex 对话执行。
- `isolation.artifact_only_context`：默认为 `true`，阶段之间只通过声明的 artifact 传递上下文。
- `global_constraints`：每个阶段都会继承的约束。
- `phases`：必须严格为 `requirements`、`design`、`tasks`、`implementation` 四个阶段。
- `phases[].goal`：prompt 的 `目标` 部分。
- `phases[].input`：prompt 的 `输入` 部分。
- `phases[].output`：prompt 的 `输出` 部分。
- `phases[].steps`：prompt 的 `步骤` 部分。
- `phases[].context_inputs`：本阶段允许读取的上游 artifact 路径，相对于目标项目根目录，例如 `doc/proposal.md`。

阶段 prompt 支持这些模板变量：

- `{user_goal}`：用户原始需求。
- `{project_root}`：目标项目目录。
- `{run_dir}`：当前 harness run 目录。
- `{phase_dir}`：当前阶段目录。
- `{conversation_dir}`：当前阶段独立对话目录，可用于自定义 Codex 包装脚本。
- `{prompt_stdin}`：在 `codex.command` 中使用，渲染为 `-`，执行时把当前阶段的 `prompt.md` 通过 stdin 传入 Codex CLI。
- `{context_files}`：当前阶段允许读取的上游 artifact。
- `{global_constraints}`：全局约束。
- `{conversation_policy}`：当前对话隔离策略说明。

## 设计原则

这个 harness 不假设复杂编排系统，也不把状态藏在长对话里。它只做最小但关键的自动化：把一个目标拆成可审计的阶段 prompt，让 Codex CLI 每个阶段从新对话开始，只看到当前阶段明确声明的上下文。
