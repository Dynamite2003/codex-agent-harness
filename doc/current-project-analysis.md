# 当前项目梳理：Coding Agent Harness

更新时间：2026-06-05

## 1. 项目介绍

Coding Agent Harness 是一个轻量级的 Codex CLI 阶段化执行框架。它的核心目标是把一个软件开发目标拆成稳定、可审计、可恢复的阶段流程，让 Codex 在每个阶段只处理当前阶段应该处理的工作，并把阶段 prompt、上下文清单、执行命令、标准输出、错误输出和状态文件都保存到磁盘。

当前项目的 Python 包名是 `codex-agent-harness`，主要入口包括：

- 命令行入口：`codex-harness` 和 `harness`。
- 本地脚本入口：仓库根目录下的 `./harness`。
- 核心代码目录：`src/codex_harness/`。
- 默认配置：`src/codex_harness/default.harness.json`。
- 示例配置：`examples/basic.harness.json`。
- 单元测试：`tests/test_harness.py`。
- 轻量 prompt skills：`skills/vibe2spec-flow`、`skills/expand-requirements-prompt`、`skills/expand-design-prompt`、`skills/expand-tasks-prompt`、`skills/expand-implementation-prompt`。
- 论文式课程报告：`doc/paper-style-report.md`。

项目当前固定支持四个软件开发阶段：

1. 需求阶段：生成 `doc/proposal.md`。
2. 设计阶段：生成 `doc/detailed-design.md`。
3. 任务阶段：生成 `doc/tasks/<module-name>.md` 和 `doc/tasks/progress.md`。
4. 实现阶段：生成 `doc/prompt.md`，作为后续轻量 Vibe Coding 的起始 prompt，默认由单个 agent 顺序实现、验证并更新任务进度。

从定位上看，它不是一个完整的多 Agent 调度平台，也不是一个通用工作流引擎；它更像是一个小而硬的工程护栏：把 Codex 的输入、输出、阶段边界、上下文传递和失败处理显式化，降低长对话和自由发挥带来的不可控性。

## 2. 项目背景

在用 AI coding agent 做真实软件开发时，常见问题包括：

- 上下文越积越长，模型容易混淆早期讨论、过期约束和当前阶段任务。
- Agent 容易在需求还没确认时直接进入设计或实现，导致返工。
- 阶段之间缺少明确产物，后续实现依赖的是聊天记忆而不是可审计文档。
- prompt 质量不稳定，同一个需求由不同人发起时，输出结构和粒度差异大。
- Codex 执行失败、追问用户或漏写产物时，如果没有状态记录，难以判断卡在哪里。
- 多人协作或长周期项目中，单靠对话历史无法形成可复现的工程流程。

Codex Agent Harness 对这些问题的解决思路是：不试图替代 Codex 的能力，而是在 Codex 外层增加一个最小阶段编排器。它把“让 Codex 做什么、可以看什么、必须产出什么、失败时如何停止”都写入配置和落盘记录中，使每次运行都能被回看和复现。

项目还特别面向 Vibe Coding 场景：先用四阶段规划生成需求、设计和任务文件，再让实现阶段生成一个轻量实现 prompt，由 Codex 后续读取 `doc/tasks/progress.md`，默认顺序实现代码、补测试并更新 checklist；只有任务独立、文件所有权清晰且上下文明显过长时，才可选启用子 agents。

## 3. 方法与技术路线

### 3.1 固定四阶段流程

项目在配置解析层强制阶段顺序必须是：

```text
requirements -> design -> tasks -> implementation
```

这个约束定义在 `src/codex_harness/config.py` 的 `REQUIRED_PHASE_IDS` 中。配置文件如果缺少阶段、阶段重复或阶段顺序不符合要求，会直接抛出配置错误。

这种设计牺牲了一部分通用工作流灵活性，但换来了更强的工程约束：需求、设计、任务、实现之间不会随意跳跃，也更容易对每个阶段做产物校验。

### 3.2 四段式阶段 prompt

每个阶段生成的 prompt 都固定为四个部分：

- 目标
- 输入
- 输出
- 步骤

`src/codex_harness/prompting.py` 负责把配置中的阶段目标、输入、输出、步骤渲染成最终 prompt，同时注入用户原始目标、项目根目录、run 目录、阶段目录、上下文文件清单、全局约束和对话隔离策略。

这种 prompt 形态的价值是稳定和可读：每个阶段都能清楚回答“这次只做什么、能参考什么、必须交付什么、按什么步骤做”。

### 3.3 Artifact-only 上下文隔离

默认配置启用：

- `new_conversation_per_phase: true`
- `artifact_only_context: true`

也就是说，每个阶段都应该是一个新的 Codex 对话，阶段之间不依赖聊天历史，只通过配置声明的 artifact 传递上下文。例如：

- 设计阶段只能读取需求阶段产出的 `doc/proposal.md`。
- 任务阶段读取 `doc/proposal.md` 和 `doc/detailed-design.md`。
- 实现阶段读取 `doc/proposal.md`、`doc/detailed-design.md` 和 `doc/tasks`。

运行时会为每个阶段生成 `context.json`，记录本阶段声明了哪些上下文输入、哪些实际存在、哪些缺失，以及预期输出是什么。

### 3.4 运行目录和审计文件

每次运行会在目标项目下创建：

```text
.harness/runs/<run-id>/
```

每个阶段目录包含：

- `prompt.md`：本阶段传给 Codex 的 prompt。
- `context.json`：本阶段允许使用的上下文和预期产物。
- `command.sh`：渲染后的 Codex CLI 命令。
- `stdout.txt`：执行模式下 Codex 标准输出。
- `stderr.txt`：执行模式下 Codex 错误输出。
- `status.json`：阶段执行状态。
- `needs-user-input.md`：如果 Codex 要求用户补充信息，则写入问题。
- `conversation/`：阶段独立对话目录的预留位置。

运行根目录还会生成 `manifest.json`，记录 run id、项目名、项目根目录、用户目标、隔离策略和所有阶段文件路径。这个文件让一次 harness 运行具备基本审计能力。

### 3.5 执行、暂停和重试机制

`src/codex_harness/runner.py` 是核心运行器。它先准备阶段文件，再根据 `execute` 参数决定是否真实调用 Codex CLI。

执行模式下支持几类关键控制：

- 命令失败：如果 Codex CLI 返回非零退出码，写入 `status.json`，标记 `command_failed` 和 `returncode`，并提示查看 `stdout.txt` / `stderr.txt`。
- 用户追问：只有当 Codex 输出独占一行的 `HARNESS_NEEDS_USER_INPUT` 时，harness 才会暂停当前阶段，并把该标记后的问题写入 `needs-user-input.md`。
- 补答重跑：用户回答会写入 `user-answers.md`，并追加到当前阶段 `prompt.md`，随后重跑同一阶段。
- 强制进入下一阶段：用户可以用 `NEXT_PHASE` 记录审计文件 `force-next-phase.md`，在当前阶段产物已足够时进入下一阶段。
- 产物缺失：如果阶段结束后缺少声明的 expected outputs，会暂停并提示用户补充重试指令。
- 缺失产物重试：重试说明会写入 `missing-output-retries.md`，并追加到当前阶段 prompt 中继续执行。
- 强制跳过阶段：用户可以用 `SKIP_PHASE` 跳过缺失产物阶段，并写入 `skip-phase.md` 作为审计记录。

这些机制让 harness 不只是生成 prompt，还具备最小的执行监督能力。此前版本曾用“请确认”“需要补充”“need clarification”等关键词辅助判断用户追问，但真实实验暴露了误触发问题：prompt 原文、搜索日志、普通总结或用户回答记录中只要出现相似词，就可能被误判为需要暂停。当前版本已经收窄为显式协议检测，只接受独占一行的 `HARNESS_NEEDS_USER_INPUT` 标记，从而降低正常日志触发暂停的概率。

### 3.6 CLI 能力

当前 CLI 支持以下子命令：

- `init-skill-flow`：初始化轻量 Vibe2Spec skill 工作流，创建项目内 quickstart 和文档目录。
- `validate-artifacts`：检查 Spec-first artifacts 是否包含必要结构和基本质量项。
- `init`：把默认 harness 配置复制到项目中的 `harness.json`。
- `run`：使用显式配置创建一次阶段化运行，可选择真实执行 Codex CLI。
- `start`：更短的入口，默认读取目标项目的 `harness.json`，没有则生成 `.harness/default.harness.json`。
- `bootstrap-python`：为 Python 项目准备 `pyproject.toml`、`ruff`、`mypy`、`pytest` 配置和 bootstrap 脚本。
- `clean-runs`：清理旧的 `.harness/runs` 目录，支持 dry-run。

此外，CLI 还有一个易用性处理：如果用户直接运行 `./harness -C /path "goal"`，没有显式写 `start` 子命令，也会被自动规范化为 `start`。

### 3.7 Python 项目启动协议

`src/codex_harness/python_bootstrap.py` 提供 Python 项目初始化能力。它会：

- 创建或补齐 `pyproject.toml`。
- 配置 `ruff`、`mypy`、`pytest`。
- 生成 `.harness/bootstrap/python-bootstrap.sh`。
- 在 `--execute` 模式下调用 `uv venv` 和 `uv add --dev ruff mypy pytest pytest-cov`。

默认配置也把 Python 项目启动协议写入全局约束：如果目标项目以 Python 为主要语言，进入 harness 前应先通过 `codex-harness bootstrap-python` 准备隔离环境和质量工具。

### 3.8 轻量 Prompt Skills

仓库内置四个轻量 skills：

- `expand-requirements-prompt`
- `expand-design-prompt`
- `expand-tasks-prompt`
- `expand-implementation-prompt`
- `vibe2spec-flow`

其中 `expand-*` skills 不运行 harness、不创建文件、不实现代码，只把一句简单需求扩展成某个阶段可复制使用的中文 prompt。`vibe2spec-flow` 则把 Spec-first 流程内化到 Codex 中，适合不启动 CLI harness、直接在当前会话里创建或更新规划 artifact 并推进实现的轻量场景。

## 4. 当前结果

### 4.1 已实现能力

当前项目已经实现了一个可运行的最小版本，能力包括：

- 可以通过 `./harness`、`harness` 或 `codex-harness` 启动。
- 可以自动查找目标项目中的 `harness.json`，没有时生成默认配置。
- 可以 dry-run 生成完整四阶段 prompt、上下文文件、命令脚本和 manifest。
- 可以 execute 真实调用 Codex CLI，并把 prompt 通过 stdin 传给 Codex。
- 可以检查每阶段 expected outputs 是否存在。
- 可以识别 Codex 显式协议式追问，并暂停阶段。
- 可以接收用户补答，追加到当前阶段 prompt 后重跑。
- 可以在产物缺失时重试、跳过或停止。
- 可以记录命令失败、用户追问、强制进入下一阶段、缺失产物跳过等审计状态。
- 可以为 Python 项目生成 uv、ruff、mypy、pytest 的基础配置。
- 可以清理旧 run 目录。
- 可以通过轻量 skills 生成单阶段 prompt。
- 默认流程吸收 Spec-first 规范，需求和设计 prompt 会要求 EARS、ADR、GIVEN-WHEN-THEN 验收标准和 spec 回填记录。
- 默认实现阶段 prompt 会先要求 agent 识别现有技术栈和可用工具，再选择验证命令，避免把 Python 项目的 `uv`、`pytest`、`mypy`、`ruff` 约束强加给静态 Web 或无依赖项目。
- 默认实现阶段 prompt 改为单 agent 顺序执行；只有任务独立、文件范围清晰且上下文明显过长时，才允许可选启用子 agents。

### 4.2 工程结构结果

当前核心模块职责如下：

| 文件 | 职责 |
| --- | --- |
| `src/codex_harness/cli.py` | CLI 参数解析、子命令分发、交互输入读取、默认配置路径处理 |
| `src/codex_harness/config.py` | JSON 配置解析、字段校验、阶段顺序约束、数据结构定义 |
| `src/codex_harness/prompting.py` | 阶段 prompt 渲染、上下文清单渲染、风格和隔离策略注入 |
| `src/codex_harness/runner.py` | run 目录创建、阶段文件生成、命令执行、状态记录、用户补答和产物缺失处理 |
| `src/codex_harness/artifact_validation.py` | Spec-first artifact 内容校验 |
| `src/codex_harness/skill_flow.py` | 轻量 skill 工作流初始化和项目 quickstart 生成 |
| `src/codex_harness/python_bootstrap.py` | Python 项目初始化、pyproject 补齐、uv bootstrap 脚本生成 |
| `src/codex_harness/defaults.py` | 从包资源读取默认 harness 配置 |
| `src/codex_harness/default.harness.json` | 默认四阶段配置 |
| `examples/basic.harness.json` | 可读示例配置，并由测试校验与包内默认配置一致 |

### 4.3 验证结果

本次梳理时执行了当前仓库验证：

```text
PYTHONPATH=src python3 -m unittest discover -s tests
结果：Ran 32 tests, OK
```

```text
.venv/bin/python -m ruff check .
结果：All checks passed!
```

```text
PYTHONPATH=src .venv/bin/python -m mypy src tests
结果：Success: no issues found
```

需要注意的是，系统级 `python3` 环境没有安装 `ruff` 和 `mypy`：

```text
python3 -m ruff check .
结果：No module named ruff

PYTHONPATH=src python3 -m mypy src tests
结果：No module named mypy
```

因此，当前环境下静态检查依赖仓库内 `.venv`，或者需要先执行 `python -m pip install -e ".[dev]"` 安装开发依赖。

### 4.4 测试覆盖结果

现有 32 个单元测试覆盖了主要行为：

- 轻量 skill flow 初始化和 quickstart 生成。
- artifact 内容校验对缺失 Spec 章节、质量要求和 Failure Mode 结构的失败报告。
- artifact 内容校验对完整 Spec-first 文档的通过判断。
- 默认 `start` 流程和无子命令自动转为 `start`。
- run 目录、阶段 prompt、context、command 文件生成。
- run id 唯一性。
- prompt style 注入。
- 上下文输入存在与缺失记录。
- 非标准阶段序列拒绝。
- 嵌套配置字段类型校验。
- 默认任务 prompt 和实现 prompt 的关键约束。
- execute 模式下真实产物校验。
- Codex 追问用户时暂停并记录。
- 普通日志中内联提到 `HARNESS_NEEDS_USER_INPUT` 或出现“请确认”等词时，不会误触发用户追问暂停。
- 用户补答后同阶段恢复执行。
- repeated questions 下强制进入下一阶段。
- 强制进入下一阶段时保留用户已输入回答。
- 缺失产物交互式重试。
- 缺失产物停止时使用明确错误类型而不是 Python traceback。
- 命令失败时写入状态文件。
- 缺失产物可审计跳过。
- Python bootstrap 配置生成。
- 包内默认配置与示例配置一致。
- 清理旧 run 目录和 dry-run 清理。
- prompt 通过 stdin 传递给执行命令。

### 4.5 CI 结果设计

仓库包含 GitHub Actions CI 配置，会在 `main` push 和 PR 上：

1. 安装 Python 3.11。
2. 执行 `python -m pip install -e ".[dev]"`。
3. 运行 `python -m ruff check .`。
4. 运行 `python -m mypy src tests`。
5. 运行 `python -m unittest discover -s tests`。

这说明项目已经有基本的持续集成闭环，能够在远端环境复现 lint、类型检查和测试。

### 4.6 近期修复结果

端到端 Web 应用对比实验暴露出两个 harness 层面的真实问题：

1. 用户追问检测过宽。旧逻辑会扫描完整 stdout/stderr，只要输出中包含 `HARNESS_NEEDS_USER_INPUT` 或命中“请确认”“需要补充”等关键词，就暂停当前阶段。真实运行中，prompt 模板、工具说明、搜索命令、用户回答记录和普通总结都可能包含这些文本，导致 harness 误判并要求人工 `NEXT_PHASE`。
2. 默认实现 prompt 过度绑定 Python 工具链。对于静态 Web 或无依赖项目，prompt 仍要求补充 pytest、通过 mypy 和 ruff，并优先使用 uv。这会把与项目无关的环境问题引入实现阶段，降低自动执行稳定性。

当前修复已经完成：

- `_detect_user_input_request` 只接受独占一行的 `HARNESS_NEEDS_USER_INPUT` 标记，并返回该行之后的问题内容。
- 移除基于自然语言关键词的追问启发式，避免普通日志误触发。
- 默认实现阶段 prompt 改为要求 agent 先识别技术栈和可用工具，再选择测试与验证方式。
- Python 工具链约束改为条件触发：只有项目已 bootstrap 或已有对应配置时，才优先使用 `uv run pytest`、`uv run mypy`、`uv run ruff check .`。
- 静态 Web 或无依赖前端项目改为要求契约测试、源码级逻辑测试、DOM smoke 或浏览器截图验证；如果浏览器或运行时不可用，需要记录原因和替代验证。
- 默认实现阶段 prompt 增加 Spec/ADR/验收标准遵守要求，并要求记录 spec 回填或实现偏离。
- 新增回归测试，确保日志里内联提到协议标记或出现“请确认”时不会暂停。

### 4.7 课程实验：Proration 计费边界案例

为了避免只用简单 Todo demo 得出不公平结论，当前项目补充了一个更容易出错的静态 Web 任务实验：[experiments/proration-vibe2spec-vs-direct-20260605](../experiments/proration-vibe2spec-vs-direct-20260605)。任务原始输入只有一句话：

> 做一个订阅升级/降级的按天计费计算器，输入当前月费、新月费、账期开始/结束日期、变更日期、优惠券和税率，输出本账期应补收或退款金额。

这个任务的难点不在 UI，而在“按天计费”背后的隐含业务规则。Direct baseline 模拟的是直接把一句需求交给 Codex 生成实现，因此产物只有 `direct-baseline/index.html` 和一份短 README；Vibe2Spec 组则先生成 `proposal.md`、`detailed-design.md`、`doc/tasks/`、`doc/prompt.md` 和 `doc/verification.md`，再按这些 artifact 实现。

实验结果如下：

| 工作流 | 功能探针结果 | 证据 |
| --- | ---: | --- |
| Direct baseline | 2 / 6 | [direct-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/direct-probe-result.json) |
| Vibe2Spec | 6 / 6 | [vibe2spec-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec-probe-result.json) |

两边都能正常渲染页面，截图分别保存在 [direct-render.png](../experiments/proration-vibe2spec-vs-direct-20260605/direct-render.png) 和 [vibe2spec-render.png](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec-render.png)。这说明 UI 是否可见并不能证明计费逻辑正确，必须用业务 fixture 验证。

Direct baseline 的主要失败原因是采用了常见但错误的简化：把每个账期固定按 30 天计算。探针暴露了三个实际计费错误：

| Case | Direct baseline | 期望结果 | 问题 |
| --- | ---: | ---: | --- |
| 2026 年 2 月，含 10% coupon 和 8.25% tax | 27.28 | 29.23 | 2026 年 2 月实际账期是 28 天，不是 30 天 |
| 2024 闰年 2 月 | 30.00 | 31.03 | 2024 年 2 月实际账期是 29 天 |
| 2026 年 1 月降级退款 | -32.00 | -30.97 | 1 月账期是 31 天，退款金额应保留负数 |

Vibe2Spec 的价值体现在它把这些隐含规则前置到了不同 artifact 中：

| Vibe2Spec 环节 | 考虑到的问题 | 对应证据 | 产生的效果 |
| --- | --- | --- | --- |
| 需求阶段 `proposal.md` | “按天计费”不能默认 30 天；变更日到期末才是受影响天数；coupon 先于 tax；tax 作用于净差额；最终金额才 round；降级为 refund；非法日期拒绝 | [Functional Requirements](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/proposal.md) | 把一句模糊需求拆成可审阅的 EARS 规则，减少实现时自由解释 |
| 验收阶段 `proposal.md` | 2026 年 2 月 28 天、2024 闰年 2 月 29 天、31 天账期降级退款、非法日期 | [Acceptance Criteria](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/proposal.md) | 把边界条件变成具体数值 fixture，例如 `29.23`、`31.03`、`-30.97` |
| 设计阶段 `detailed-design.md` | JavaScript 日期解析可能受时区或 DST 影响；退款不应丢失符号 | [ADR: UTC Date-Only Arithmetic](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/detailed-design.md) | 实现采用 UTC date-only day difference，并保留负数 refund |
| 实现 prompt `doc/prompt.md` | 编码阶段不能重新自由发挥，要遵循 Spec / ADR / Acceptance Criteria | [Implementation Prompt](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/prompt.md) | 实现阶段有明确输入和验证要求，并暴露 `window.calculateProration` 供探针调用 |
| 验证阶段 `doc/verification.md` 与 `probe_proration.py` | 页面可渲染不代表业务正确，需要直接验证计算核心 | [verification.md](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/verification.md)、[probe_proration.py](../experiments/proration-vibe2spec-vs-direct-20260605/probe_proration.py) | Vibe2Spec 通过全部 6 项探针；Direct baseline 虽能渲染但只通过 2 项 |

因此，这个实验展示的优势不是“文档更多”，而是 Spec-first 把模糊业务意图转化为需求规则、设计决策、验收 fixture 和可执行验证。对于简单 Todo 任务，Direct Codex 和 Vibe2Spec 可以打平；但当任务存在真实业务边界时，Vibe2Spec 能更早暴露隐含假设，并把错误从“上线后计算错”前移到“实现前或验证时被 fixture 拦住”。

这个实验仍有边界：Direct baseline 是仓库中的 direct-style 对照产物，不是多次独立随机采样的 Codex 运行结果。更严格的课程展示可以扩展为多次 direct sample 与多次 Vibe2Spec sample 的平均通过率、返工轮数和漏需求数量对比。

## 5. 项目意义

### 5.1 对 AI 软件开发流程的意义

这个项目的核心意义在于把 AI coding 从“连续聊天”推进到“阶段化工程流程”。它要求每个阶段都有明确输入和产物，后续阶段只依赖前序 artifact，而不是依赖模型记忆。这种方式更接近真实软件工程中的需求评审、架构设计、任务拆分和实现交付。

### 5.2 对可审计性的意义

每次运行都会留下 prompt、context、command、stdout、stderr、status 和 manifest。出现问题时，可以定位是 prompt 不清楚、上下文缺失、Codex 命令失败、用户问题未回答，还是阶段产物没有生成。这比只看最终代码或聊天记录更容易追踪原因。

### 5.3 对可复现性的意义

配置、prompt 和命令都落盘后，同一个目标可以在不同时间、不同机器或不同人手上复查和复跑。即使执行结果受模型波动影响，至少输入结构和阶段约束是可复现的。

### 5.4 对上下文管理的意义

Artifact-only 模式能显著减少长上下文污染。每个阶段的新对话只接收声明文件，避免上一阶段的讨论细节、废弃方案或未确认猜测继续影响后续输出。

### 5.5 对 Vibe Coding 的意义

项目最后阶段不是直接写代码，而是生成轻量实现 prompt `doc/prompt.md`。这让前期规划和后期实现之间形成衔接：先把任务拆细、写入 `doc/tasks/progress.md`，再让 Codex 根据进度文件顺序实现、验证和回写；多 agent 并行只作为大任务下的可选策略。

### 5.6 对团队协作的意义

需求、设计、任务和实现 prompt 都是文件，团队成员可以在 PR 中审阅这些 artifact。相比“某个人和模型聊出来的结果”，这种文件化产物更适合多人协作、代码评审和过程复盘。

## 6. 当前不足与风险

### 6.1 阶段固定，通用性有限

项目强制四阶段顺序，这对软件开发很清晰，但也限制了通用工作流扩展。例如调研、评审、迁移、发布、回滚等阶段目前不能作为一等公民配置进去。

这种限制是当前版本的设计取舍：先保证核心开发流程稳定，再考虑扩展。

### 6.2 产物校验仍是轻量启发式

当前 harness 已经不只检查文件或目录是否存在。`artifact_validation.py` 会对 `doc/proposal.md`、`doc/detailed-design.md`、`doc/tasks/` 和 `doc/prompt.md` 做轻量内容校验，覆盖 EARS、ADR、GIVEN-WHEN-THEN、Product Archetype、Success Mode、Failure Modes、Behavioral Requirements、Quality Requirements、验证策略和任务追溯等关键结构。

但这仍然是关键词/概念组级别的启发式检查，不能证明文档内容真的完整、正确或可执行。后续可以考虑增加结构化 schema、标题层级检查、最小内容长度、验收 fixture 解析、ADR 完整性检查或自定义 validator。

### 6.3 Codex 追问检测已收窄，但协议仍偏轻量

当前版本已经取消自然语言关键词启发式，只接受独占一行的 `HARNESS_NEEDS_USER_INPUT`。这解决了实验中暴露的误触发问题，但协议仍是轻量文本协议：

- 如果 Codex 忘记输出该独占行，harness 不会自动暂停。
- 如果 Codex 把问题写在正文但没有协议标记，harness 会继续进入产物校验。
- 如果未来需要更强可靠性，仍应引入结构化状态文件或 JSON status。

因此，当前修复重点是降低误判；漏判风险需要通过更严格的阶段输出协议继续解决。

### 6.4 没有真正管理 Codex conversation 状态

每个阶段创建了 `conversation/` 目录，并在 prompt 中说明新对话隔离策略，但当前实现本身并不直接控制 Codex CLI 的真实会话存储或 resume 行为。是否完全新对话，仍取决于渲染后的 Codex 命令和 Codex CLI 行为。

如果未来需要严格隔离，需要结合 Codex CLI 的会话参数或包装脚本进一步实现。

### 6.5 执行安全边界较粗

默认 Codex 命令使用 `--sandbox workspace-write` 和 `--skip-git-repo-check`。这能降低目标项目不是 git 仓库时的摩擦，但也意味着用户需要理解执行 Codex CLI 会真实修改 workspace。

当前 harness 主要负责阶段边界，不负责更细粒度的文件写入策略、安全审批或命令白名单。

### 6.6 缺少 resume 已有 run 的能力

当前 `create_run` 每次都会创建新 run 目录。虽然单阶段内部可以补答和重试，但如果进程退出后想从某个已有 run 的阶段继续，目前没有完整的 resume 命令。

后续可以增加：

- `resume --run-dir ...`
- 从 `manifest.json` 恢复阶段状态。
- 跳过已完成阶段。
- 只重跑指定阶段。

### 6.7 子 Agent 仍只是可选提示能力

实现阶段现在默认生成单 agent 顺序执行 prompt，并只在任务独立、文件范围清晰且上下文明显过长时允许可选启用子 agents。当前 harness 自身仍不调度子 agents，也不跟踪子任务执行结果；多 Agent 实现仍停留在 prompt 约束层，而不是 harness 的运行时能力。

如果要把它做成完整平台，需要增加任务队列、子进程管理、并发控制、结果合并、冲突处理和失败重试。

### 6.8 缺少更丰富的真实项目样例

当前示例配置主要展示 harness 自身流程，没有包含完整目标项目从一句需求到最终实现的端到端样例。对于新用户来说，理解 artifact 链路和最佳实践仍需要阅读 README 与测试。

后续可以增加一个 `examples/demo-project`，展示：

- 原始用户目标。
- 四阶段输出文档。
- 生成的实现 prompt。
- 一次 dry-run 和 execute 的 run 目录结构。

### 6.9 文档仍偏工具说明，缺少设计决策记录

README 已覆盖使用方式，但项目层面的架构决策、取舍理由、失败模式和未来路线尚未形成正式 ADR 或设计文档。本文件补充了当前梳理，但后续仍建议拆出更稳定的 `doc/architecture.md`、`doc/roadmap.md` 和 `doc/adr/`。

## 7. 后续改进建议

1. 增加 `resume` 能力，让中断后的 run 可以从指定阶段继续。
2. 增强 artifact 内容校验，例如结构化 schema、验收 fixture 解析和 ADR 完整性检查。
3. 支持可选阶段扩展，在保持默认四阶段的同时允许用户添加 review、release 等阶段。
4. 引入结构化阶段状态输出，在当前独占行协议基础上进一步减少漏判。
5. 明确 Codex conversation 隔离实现方式，必要时封装 Codex CLI 会话参数。
6. 增加端到端 demo 项目，让用户看到完整 artifact 链。
7. 增加文档化设计决策记录，解释为什么固定四阶段、为什么 artifact-only、为什么实现阶段只生成轻量实现 prompt。
8. 改进安全策略，例如在 execute 前预览即将运行的命令，或支持更细粒度的允许写入路径。
9. 为轻量 skills 增加测试或同步校验，避免 skills 模板和默认 harness 配置长期漂移。

## 8. 总结

当前项目已经形成一个清晰的 0.1.0 版本：它用少量 Python 代码实现了四阶段 Codex CLI harness，具备配置解析、prompt 生成、上下文隔离、运行审计、产物校验、交互暂停、缺失产物重试、Python bootstrap 和基础 CI。

它的优势是边界清楚、结构简单、工程约束强，适合把 AI coding 流程从临时聊天沉淀为可审阅的文档链路和运行记录。它的主要不足是验证仍偏浅、阶段扩展有限、conversation 隔离和可选多 Agent 调度还没有成为真实运行时能力。

总体看，这个项目已经适合作为 Vibe Coding 前置规划和 Codex CLI 阶段化执行的基础工具；下一阶段的关键是增强恢复能力、内容质量校验和真实端到端样例。
