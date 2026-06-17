# Codex Agent Harness

一个轻量的 Codex CLI harness，用来把软件开发任务拆成阶段执行，并把阶段上下文、prompt 和命令脚本落盘。

当前框架提供：

- 轻量 Codex skill 工作流：把 Spec-first 流程内化到 Codex 中，适合日常快速规划和实现，不需要等待完整 harness CLI 四阶段执行。
- 固定四阶段开发：每个具体需求都会拆成 `需求 -> 设计 -> 任务 -> 实现`。
- 四段式阶段 prompt：每个阶段发给 Codex 的 prompt 都只有 `目标`、`输入`、`输出`、`步骤` 四个部分。
- 隔离上下文：每个阶段默认开启新的 Codex 对话，只接收用户目标、全局约束，以及配置中声明的上游 artifacts。
- 自动润色 prompt：把原始目标整理成可直接交给 Codex CLI 的阶段化结构化 prompt。
- Python 项目启动协议：先用 `uv` 隔离环境，并配置 `ruff`、`mypy`、`pytest`。

## 快速开始

从源码安装命令行工具：

```bash
python3 -m pip install -e .
```

如果要运行 lint、类型检查和测试，安装开发依赖：

```bash
python3 -m pip install -e ".[dev]"
make check
```

推荐日常使用轻量 skill 工作流。先安装并初始化：

```bash
codex-harness init-skill-flow --path /path/to/project
```

然后在 Codex 里直接说：

```text
$vibe2spec-flow 给现有 Web 项目增加登录页
```

这会在当前 Codex 会话中按 Spec-first 流程创建或更新 `doc/proposal.md`、`doc/detailed-design.md`、`doc/tasks/`，并默认用单 agent 顺序实现和验证。需要人工确认的问题会写入文档，不会强制等待完整 CLI harness 四阶段执行。

检查当前 artifact 内容质量：

```bash
codex-harness validate-artifacts -C /path/to/project
```

只有需要完整审计、stdout/stderr、阶段状态和失败复跑时，再使用 CLI harness 高级模式：

```bash
./harness -C /path/to/project "给现有 Web 项目增加登录页"
```

这会使用默认配置，真实执行四个阶段。`-C` 是目标项目目录；如果不传 `-C`，默认使用当前目录。

只想预览每阶段 prompt，不调用 Codex：

```bash
./harness -C /path/to/project --dry-run "给现有 Web 项目增加登录页"
```

如果已经安装了包，也可以使用更短的入口：

```bash
harness -C /path/to/project "给现有 Web 项目增加登录页"
```

生成课程项目报告 PDF：

```bash
mkdir -p tmp/pdfs/texbuild output/pdf
.tinytex/TinyTeX/bin/universal-darwin/xelatex \
  -interaction=nonstopmode \
  -halt-on-error \
  -output-directory=tmp/pdfs/texbuild \
  doc/course-project-report.tex
cp tmp/pdfs/texbuild/course-project-report.pdf output/pdf/course-project-report.pdf
```

课程展示样例：

- 中文 LaTeX 课程项目报告：[doc/course-project-report.tex](doc/course-project-report.tex)
- 已生成 PDF：[output/pdf/course-project-report.pdf](output/pdf/course-project-report.pdf)
- 论文式项目报告：[doc/paper-style-report.md](doc/paper-style-report.md)
- 完整 demo 项目：[examples/demo-project](examples/demo-project)
- 简单 Todo 对比：[experiments/vibe2spec-vs-direct-20260605/REPORT.md](experiments/vibe2spec-vs-direct-20260605/REPORT.md)，两边功能打平，主要展示 artifact 链路。
- 复杂计费边界对比：[experiments/proration-vibe2spec-vs-direct-20260605/REPORT.md](experiments/proration-vibe2spec-vs-direct-20260605/REPORT.md)，Direct baseline `2/6`，Vibe2Spec `6/6`，用于展示 Spec-first 对隐含业务规则的收益。

默认配置查找顺序：

- 目标项目下的 `harness.json`
- 自动生成的 `.harness/default.harness.json`

自动生成的默认配置来自包内 `codex_harness/default.harness.json`。仓库里的
[examples/basic.harness.json](examples/basic.harness.json) 是同一份配置的可读示例，测试会校验两者保持一致。

dry-run 只生成 harness 审计文件，不调用 Codex CLI，也不会生成 `doc/` 下的阶段产物。生成内容位于：

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
- `implementation`：生成轻量 Vibe Coding 起始 prompt `doc/prompt.md`，默认由单个 agent 根据 `doc/tasks/progress.md` 顺序实现、验证并更新 checklist；只有任务独立且上下文规模明显需要时，才建议可选使用子 agents。

## 轻量 Prompt Skills

完整 harness 会让四个阶段分别启动 Codex，并把上下文、prompt、stdout/stderr 和阶段产物全部落盘，适合需要审计、可恢复、多人协作或严格产物校验的开发流程。早期创意探索只想把一句话扩展成某个阶段的完整 prompt 时，可以直接使用仓库内置的轻量 skills，避免完整四阶段执行带来的额外 token 开销。

日常使用更推荐从 `$vibe2spec-flow` 开始：它不启动 harness CLI，而是在当前 Codex 会话中直接读取项目、创建或更新 `doc/proposal.md`、`doc/detailed-design.md`、`doc/tasks/`、`doc/prompt.md`，并按 Spec-first 规则推进实现。只有需要完整运行审计、阶段 stdout/stderr、失败恢复记录或 CI 风格复跑时，再使用 `./harness`。

手动安装到本机 Codex skills 目录：

```bash
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

更推荐用初始化命令安装并创建 `doc/specs`、`doc/tasks` 和 quickstart：

```bash
codex-harness init-skill-flow --path .
```

可用 skills：

- `$vibe2spec-flow`：轻量 Spec-first 工作流，直接在 Codex 中完成需求、设计、任务、实现或 prompt 生成，不运行 harness CLI。
- `$expand-requirements-prompt`：把一句产品想法扩展成需求阶段 prompt，目标产物为 `doc/proposal.md`。
- `$expand-design-prompt`：把需求文档扩展成详细设计阶段 prompt，目标产物为 `doc/detailed-design.md`。
- `$expand-tasks-prompt`：把需求和设计扩展成任务拆分 prompt，目标产物为 `doc/tasks/`。
- `$expand-implementation-prompt`：把规划 artifacts 扩展成轻量实现 prompt，默认单 agent 顺序编码、测试和更新进度。

示例：

```text
$expand-requirements-prompt 我想做一个 AI 考试比赛时间轴提醒 Web 应用
```

`expand-*` skills 只生成可复制的阶段 prompt，不会自动运行 harness、创建项目或修改业务代码。`$vibe2spec-flow` 是日常默认路径，可以直接在 Codex 当前会话里创建 artifact 或继续实现。需要完整阶段审计时，再使用 `./harness -C /path/to/project "..."`。

高级用法仍然可以显式指定配置：

```bash
codex-harness run --config examples/basic.harness.json --project-root /path/to/project --goal "..." --execute
```

执行模式会真实调用 Codex CLI，并按阶段检查目标项目中的产物：

- `requirements` 必须生成 `doc/proposal.md`。
- `design` 必须生成 `doc/detailed-design.md`。
- `tasks` 必须生成 `doc/tasks/` 和 `doc/tasks/progress.md`。
- `implementation` 必须生成 `doc/prompt.md`。

如果某个阶段完成后缺少声明的产物，harness 会失败并在该阶段目录写入 `status.json`。

默认 Spec-first 阶段还会做内容校验：`doc/proposal.md` 需要包含 EARS、ADR Candidates、GIVEN-WHEN-THEN、Product Archetype、Success Mode、Failure Modes、Behavioral Requirements、Quality Requirements、Verification Strategy 等关键结构；`doc/detailed-design.md`、`doc/tasks/` 和 `doc/prompt.md` 也会检查基本质量项与成功模式/失败模式/质量追溯。你也可以随时运行 `codex-harness validate-artifacts -C /path/to/project` 单独校验。

如果 Codex CLI 命令本身返回非零退出码，harness 不会直接打印 Python traceback，而是会在当前阶段写入
`status.json`，标记 `command_failed` 和 `returncode`，并提示查看该阶段的 `stdout.txt` / `stderr.txt`。

如果 Codex 在某个阶段输出独占一行的 `HARNESS_NEEDS_USER_INPUT`，执行模式会在同一个进程中暂停当前阶段，打印该标记后的问题并等待你输入回答。输入多行回答后，用单独一行 `END` 提交；harness 会把回答记录到 `user-answers.md`，追加到当前阶段 `prompt.md`，重新执行同一阶段。只有当前阶段不再请求补充且产物校验通过后，才会进入下一阶段。普通日志或 prompt 文本里内联提到该标记不会触发暂停。

如果 Codex 反复追问但你认为当前阶段产物已经足够，可以输入单独一行 `NEXT_PHASE`。如果你在 `NEXT_PHASE` 前已经输入了回答，harness 会先把这些回答记录到 `user-answers.md`，再校验当前阶段声明的产物；产物存在则进入下一阶段，同时写入 `force-next-phase.md` 作为审计记录。

如果某阶段结束后缺少声明产物，例如 design 阶段没有生成 `doc/detailed-design.md`，harness 不会打印 Python traceback，而是会暂停并列出缺失文件。你可以输入补充指令并用 `END` 提交，harness 会把指令追加到当前阶段 prompt 并重跑该阶段；也可以输入 `SKIP_PHASE` 强制跳过并写入 `skip-phase.md`；输入 `STOP` 则停止。产物缺失时默认不会空跳阶段。

本地开发时运行测试：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

安装开发依赖后可以使用统一入口：

```bash
python3 -m pip install -e ".[dev]"
make check
```

`make check` 会依次运行单元测试、ruff 和 mypy。仓库也包含 GitHub Actions CI，会在 `main` push 和 PR 上运行同一套检查。

清理旧的 harness 审计运行目录：

```bash
./harness clean-runs -C /path/to/project --keep 10
./harness clean-runs -C /path/to/project --keep 10 --dry-run
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
