# Vibe2Spec：面向 Codex 的 Spec-first 软件开发流程与课程项目实验报告

更新时间：2026-06-05

## 摘要

大语言模型驱动的软件开发可以快速生成可运行代码，但在需求含糊、业务边界隐含、上下文较长或需要多人复盘时，直接对话式开发容易出现规则遗漏、过程不可追踪和验证不足的问题。Vibe2Spec 的目标是在不替代 Codex 编码能力的前提下，为 Codex 增加一层轻量 Spec-first 工程流程：先把一句需求沉淀为需求、设计、任务、实现 prompt 和验证记录，再由 Codex 按 artifact 顺序实现。

当前项目实现了两条路径：一条是完整 CLI harness，用于需要阶段审计、stdout/stderr、失败恢复和产物校验的场景；另一条是更轻量的 Codex skill 工作流 `$vibe2spec-flow`，把 Spec-first 流程内化到 Codex 当前会话中，避免每次都启动完整四阶段 harness。实验结果显示：在简单 Todo deadline 任务上，Direct baseline 与 Vibe2Spec 都通过 16/16 功能探针，说明简单任务不一定需要重流程；在更容易出错的订阅 proration 计费任务上，Direct baseline 只通过 2/6，Vibe2Spec 通过 6/6，优势来自需求阶段和验收阶段提前显式化真实账期天数、闰年、coupon-before-tax、final-only rounding 和退款符号等隐含规则。

因此，本项目的课程价值不在于构建一个复杂多 Agent 平台，而在于展示一种可运行、可验证、可复盘的 AI coding 工程方法：把模糊需求转化为可审阅 Spec，把隐含边界转化为验收 fixture，把实现过程转化为可追踪 artifact 链路。

关键词：AI Coding；Codex；Spec-first；Vibe Coding；软件工程流程；需求工程；可验证开发

## 1. 引言

### 1.1 研究背景

直接使用 Codex 开发软件时，常见工作方式是用户输入一段自然语言需求，Codex 立即阅读代码、修改文件并运行测试。这种方式在小任务中效率很高，但当任务包含复杂业务规则或长期演进时，会暴露几个问题：

- 需求未结构化，模型可能按常见经验补全规则，遗漏真实边界。
- 设计决策停留在聊天上下文里，后续实现和复盘难以追踪。
- 任务拆分和验证标准不明确，容易出现“页面可见但业务逻辑错误”。
- 长对话会混入废弃假设、旧约束和临时讨论，影响后续判断。
- 如果 Codex 失败、追问或漏写产物，缺少统一状态记录。

这些问题并不说明 Codex 编码能力不足，而是说明直接对话式开发缺少工程化外壳。Vibe2Spec 尝试补上这个外壳。

### 1.2 研究问题

本项目围绕三个问题展开：

1. 如何把一句自然语言开发需求转化为可审阅、可实现、可验证的 artifact 链？
2. 如何在不强制多 Agent、不显著拖慢日常开发的情况下，把 Spec-first 流程内化到 Codex 使用体验中？
3. 在什么任务上，Vibe2Spec 相比直接 Codex 开发能体现实际收益？

### 1.3 项目贡献

当前项目形成了以下可运行贡献：

- 实现了 `requirements -> design -> tasks -> implementation` 四阶段 CLI harness。
- 将阶段输入、prompt、上下文清单、执行命令、stdout/stderr、状态文件和 manifest 落盘。
- 增加了 `$vibe2spec-flow` 轻量 skill，让日常使用默认不启动完整 harness。
- 引入 artifact 内容校验，检查 `proposal.md`、`detailed-design.md`、`doc/tasks/` 和 `doc/prompt.md` 的 Spec-first 结构，并覆盖 Product Archetype、Success Mode、Failure Modes、Behavioral Requirements、Quality Requirements 等质量镜头。
- 默认实现阶段改为单 agent 顺序执行，subagents 只作为上下文过大或任务独立时的可选策略。
- 通过 Todo、Sprint Board、Proration 三组实验区分了“小任务打平”“复杂 UI 流程有过程收益”“隐含业务边界有功能收益”三类情况。

## 2. 方法设计

### 2.1 总体思路

Vibe2Spec 的核心假设是：AI coding 的关键风险往往不是“不会写代码”，而是“没有先定义清楚要写什么、为什么这样写、怎么判断写对”。因此项目把开发过程拆成四类 artifact：

| 阶段 | 产物 | 作用 |
| --- | --- | --- |
| 需求 | `doc/proposal.md` | 将一句需求转化为背景、目标、非目标、EARS 需求、ADR 候选、验收标准、风险和待确认问题 |
| 设计 | `doc/detailed-design.md` | 明确模块职责、数据模型、接口契约、关键 ADR、流程、UI 状态和测试策略 |
| 任务 | `doc/tasks/`、`doc/tasks/progress.md` | 把设计拆成可执行 checklist，并记录实现进度 |
| 实现 | `doc/prompt.md`、`doc/verification.md` | 给 Codex 一个轻量实现 prompt，并记录验证结果和偏离情况 |

这些 artifact 是阶段之间传递上下文的主渠道。后续阶段不依赖“上一轮聊天记忆”，而依赖已经落盘、可审阅的文件。

### 2.2 CLI Harness 路径

完整 harness 适合需要审计和复跑的场景。它会在目标项目下创建：

```text
.harness/runs/<run-id>/
```

每个阶段目录包含 `prompt.md`、`context.json`、`command.sh`、`stdout.txt`、`stderr.txt`、`status.json` 和可选的 `needs-user-input.md`。运行根目录包含 `manifest.json`，用于记录本次运行的用户目标、项目路径、阶段文件和隔离策略。

该路径解决的问题是可审计性和失败定位：当阶段失败时，可以判断是 Codex 命令失败、用户信息不足、产物缺失，还是 artifact 内容不合格。

### 2.3 轻量 Skill 路径

真实使用中，完整 harness 每个阶段都启动 Codex、等待 stdout/stderr 和产物校验，会带来明显等待成本。根据实验反馈，当前项目将日常默认路径调整为 `$vibe2spec-flow`：

- 不启动完整 harness CLI。
- 直接在当前 Codex 会话中创建或更新 `doc/proposal.md`、`doc/detailed-design.md`、`doc/tasks/`、`doc/prompt.md`。
- 默认单 agent 顺序实现和验证。
- 只有需要完整运行审计、失败恢复、CI 风格复跑时，再切换到 CLI harness。

这个调整使项目从“强行编排 Codex”转为“把 Spec-first 工作习惯内化为 Codex skill”。它保留了 Spec 的收益，同时降低了日常使用成本。

### 2.4 关键工程约束

当前版本采用几条保守约束：

- 阶段固定为需求、设计、任务、实现，避免流程自由跳跃。
- 阶段 prompt 固定为“目标、输入、输出、步骤”四段，提升可读性。
- 上下文传递以 artifact 为主，减少长对话污染。
- 实现阶段默认单 agent，避免小任务中过度并发和文件冲突。
- 用户追问只接受独占一行的 `HARNESS_NEEDS_USER_INPUT`，避免普通日志误触发。
- 静态 Web 或无依赖项目不强制 `uv`、`pytest`、`mypy`、`ruff`，而要求选择与技术栈匹配的验证方式。

## 3. 系统实现

### 3.1 模块结构

核心代码位于 `src/codex_harness/`：

| 文件 | 职责 |
| --- | --- |
| `cli.py` | CLI 参数解析、子命令分发、交互输入读取、默认配置处理 |
| `config.py` | JSON 配置解析、字段校验、阶段顺序约束 |
| `prompting.py` | 阶段 prompt 渲染、上下文清单渲染、隔离策略注入 |
| `runner.py` | run 目录创建、阶段文件生成、命令执行、状态记录、用户补答和产物缺失处理 |
| `artifact_validation.py` | Spec-first artifact 内容校验 |
| `skill_flow.py` | 初始化轻量 skill 工作流和项目内 quickstart |
| `python_bootstrap.py` | Python 项目 `uv`、`ruff`、`mypy`、`pytest` bootstrap |
| `defaults.py` | 读取包内默认 harness 配置 |
| `default.harness.json` | 默认四阶段配置 |

配套资源包括：

- `skills/vibe2spec-flow/`
- `skills/expand-requirements-prompt/`
- `skills/expand-design-prompt/`
- `skills/expand-tasks-prompt/`
- `skills/expand-implementation-prompt/`
- `examples/demo-project/`
- `experiments/*`

### 3.2 CLI 能力

当前 CLI 支持：

- `codex-harness init-skill-flow --path <project>`：安装轻量 skill 工作流并初始化项目文档目录。
- `codex-harness validate-artifacts -C <project>`：检查 Spec-first artifact 的结构质量。
- `codex-harness init`：生成 `harness.json`。
- `codex-harness run --execute`：按显式配置运行完整阶段流程。
- `codex-harness start` 或 `./harness -C <project> "goal"`：使用默认配置启动。
- `codex-harness bootstrap-python`：为 Python 项目生成隔离环境和质量工具配置。
- `codex-harness clean-runs`：清理旧 run 目录。

### 3.3 验证机制

验证分为三层：

1. 工程验证：单元测试、ruff、mypy、CI。
2. Artifact 验证：检查 proposal、design、tasks、prompt 是否包含必要结构。
3. Demo 验证：对目标应用运行功能探针和 Chrome headless 渲染截图。

截至 2026-06-05，仓库验证结果为：

```text
.venv/bin/python -m ruff check .
结果：通过

PYTHONPATH=src .venv/bin/python -m mypy src tests
结果：通过

PYTHONPATH=src python3 -m unittest discover -s tests
结果：32 tests OK
```

这些检查说明项目本身已经具备基本工程质量闭环。

## 4. 实验设计

### 4.1 实验目标

实验不试图证明 Vibe2Spec 在所有任务上都优于 Direct Codex。更公平的问题是：

- 对简单任务，Spec-first 是否会带来过重成本？
- 对复杂 UI 任务，Spec-first 是否提升过程可追踪性和验证质量？
- 对隐含业务规则任务，Spec-first 是否减少边界条件遗漏？

因此项目保留了三类实验。

### 4.2 实验一：Todo Deadline

实验目录：[experiments/vibe2spec-vs-direct-20260605](../experiments/vibe2spec-vs-direct-20260605)

任务：给无依赖 Todo Web App 增加“截止时间 + 逾期标记”能力。

结果：

| 工作流 | 功能探针 |
| --- | ---: |
| Direct baseline | 16 / 16 |
| Vibe2Spec | 16 / 16 |

结论：这个任务太简单，两边功能打平。Vibe2Spec 的收益不是功能更强，而是产物链更完整，包括 proposal、spec、design、tasks、prompt 和 verification。这个实验适合展示流程，不适合证明功能优势。

### 4.3 实验二：Sprint Board Lite

实验目录：[experiments/web-harness-vs-direct-20260603](../experiments/web-harness-vs-direct-20260603)

任务：实现一个无依赖静态 Web 看板应用，包含任务新增、四列看板、状态流转、筛选、KPI、本地持久化和 JSON 导入导出。

结果摘要：

| 维度 | Direct Codex | Harness Flow |
| --- | --- | --- |
| 功能完整性 | 契约测试 6/6 | 契约测试 6/6，并补充 focused tests、Node-backed 逻辑断言和 DOM smoke |
| 桌面端信息架构 | 可用，但 JSON 区被截断、留白明显 | 更像工作台，表单、筛选、导入导出和看板层级更清楚 |
| 移动端 | 不合格 | 仍有裁切，未完全合格 |
| 可追踪性 | 缺少需求/设计/任务链路 | proposal、detailed-design、tasks、prompt、verification 全链路可追溯 |
| 成本 | 快、简单 | 更慢，需要处理 harness 误触发和环境问题 |

结论：这个实验不能证明 harness 功能碾压 direct，但暴露了真实工程问题，并推动了后续修复：追问协议收窄、实现 prompt 不再强制 Python 工具链、subagents 从默认方案降级为可选方案。

### 4.4 实验三：Proration 计费边界

实验目录：[experiments/proration-vibe2spec-vs-direct-20260605](../experiments/proration-vibe2spec-vs-direct-20260605)

任务原始输入：

> 做一个订阅升级/降级的按天计费计算器，输入当前月费、新月费、账期开始/结束日期、变更日期、优惠券和税率，输出本账期应补收或退款金额。

这个任务的难点是“按天计费”背后的隐含规则：真实账期天数、闰年 2 月、coupon-before-tax、tax on net delta、final-only rounding、负数退款和非法日期拒绝。

功能探针结果：

| 工作流 | 探针结果 | 证据 |
| --- | ---: | --- |
| Direct baseline | 2 / 6 | [direct-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/direct-probe-result.json) |
| Vibe2Spec | 6 / 6 | [vibe2spec-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec-probe-result.json) |

Direct baseline 的主要失败是把账期固定为 30 天：

| Case | Direct baseline | Vibe2Spec / 期望 | 说明 |
| --- | ---: | ---: | --- |
| 2026 年 2 月，10% coupon，8.25% tax | 27.28 | 29.23 | 2026 年 2 月实际账期为 28 天 |
| 2024 闰年 2 月 | 30.00 | 31.03 | 2024 年 2 月实际账期为 29 天 |
| 2026 年 1 月降级退款 | -32.00 | -30.97 | 1 月账期为 31 天，退款保留负数 |

Vibe2Spec 在不同阶段提前处理了这些问题：

| 环节 | 处理的问题 | 证据 | 效果 |
| --- | --- | --- | --- |
| 需求阶段 | 实际账期天数、变更日、coupon、tax、round、refund、非法日期 | [proposal.md](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/proposal.md) | 模糊“按天计费”被拆成 EARS 规则 |
| 验收阶段 | 28 天 2 月、29 天闰年、31 天退款、非法日期 | [proposal.md](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/proposal.md) | 边界条件变成具体 fixture：29.23、31.03、-30.97 |
| 设计阶段 | JS 日期解析时区风险、退款符号保留 | [detailed-design.md](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/detailed-design.md) | 采用 UTC date-only day difference，返回负数 refund |
| 实现阶段 | 不重新自由解释需求 | [prompt.md](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec/doc/prompt.md) | 要求遵循 Spec / ADR / Acceptance Criteria |
| 验证阶段 | UI 渲染不等于计费正确 | [probe_proration.py](../experiments/proration-vibe2spec-vs-direct-20260605/probe_proration.py) | 直接调用 `calculateProration` 验证核心逻辑 |

结论：这个实验是当前项目最能体现 Vibe2Spec 价值的 case。优势不来自文档数量，而来自 Spec-first 将隐含业务规则前置为可执行验收标准。

## 5. 讨论

### 5.1 相比直接 Codex 的优势

Vibe2Spec 的优势不是让模型“更会写代码”，而是改变输入质量和验证边界：

- Direct Codex 适合需求清楚、风险低、反馈快的小任务。
- Vibe2Spec 适合业务规则隐含、后续要维护、需要复盘或多人审阅的任务。
- 当边界条件没有写进 prompt 时，模型可能按常见经验实现，例如把账期当作 30 天。
- 当边界条件写成验收 fixture 后，错误会在实现前或验证时暴露。

因此，是否使用 Vibe2Spec 应按任务风险选择，而不是强制所有任务走重流程。

### 5.2 相比 OpenSpec 类方法的差异

本项目不以“替代 OpenSpec”作为目标。它的差异主要在使用位置和集成方式：

- 更贴近 Codex 本地开发：直接围绕 Codex CLI、Codex skill 和本地文件系统设计。
- 更轻量：日常默认使用 `$vibe2spec-flow`，不强制完整平台化流程。
- 更强调 artifact 到实现 prompt 的闭环：最终产物不是停在 spec，而是生成可执行的 Codex 实现指令。
- 更适合课程项目展示：可以用实验目录、probe JSON、截图和验证命令形成可复盘证据链。

代价是：当前项目的规范能力、生态成熟度和通用协作能力仍弱于大型开源规范框架。

### 5.3 为什么不默认使用 Subagents

早期方案倾向用 subagents 分工实现，但实验显示这对当前项目偏重：

- 小任务中 subagents 带来等待和上下文管理成本。
- 并发写文件需要更强 ownership 和合并协议，否则可能出现短暂文件覆盖或中间态。
- 当前 harness 自身并不调度 subagents，也不跟踪子任务结果。

因此当前版本把 subagents 降级为可选策略：只有任务独立、文件范围清晰、上下文明显过长时才建议使用。默认路径是单 agent 顺序执行。

## 6. 局限性

当前项目仍有明确边界：

- 实验样本少，不能得出统计意义上的通用结论。
- Direct baseline 是仓库中的 direct-style 对照产物，不是多次随机新 Codex 会话采样。
- Artifact 内容校验仍是轻量结构检查，不能完全替代人工评审。
- CLI harness 的 conversation 隔离目前主要体现在 prompt 和目录结构上，仍依赖 Codex CLI 的真实会话行为。
- Resume 已有 run 的能力还不完整。
- 安全边界仍较粗，harness 不负责细粒度文件写入审批。
- 移动端 UI 质量在 Sprint Board 实验中仍未完全解决。

这些局限意味着当前项目更适合作为 Spec-first AI coding 方法的课程原型，而不是生产级多 Agent 平台。

## 7. 后续工作

后续优先级建议如下：

1. 增加 `resume --run-dir`，支持中断后从已有 run 继续。
2. 增强 artifact 内容校验，例如结构化 schema、验收标准 fixture 解析、ADR 完整性检查。
3. 为 `$vibe2spec-flow` 增加同步测试，避免 skill 模板和默认 harness 配置漂移。
4. 设计更严格的 direct vs Vibe2Spec 多样本实验，统计首轮通过率、漏需求数量、返工轮数和耗时。
5. 将 proration case 扩展为课程展示脚本，包括输入、运行命令、截图、probe 结果和讲解稿。
6. 明确 Codex conversation 隔离策略，必要时封装 Codex CLI 会话参数。
7. 如果未来重新引入 subagents，需要增加写域 ownership、合并协议、冲突检测和失败重试。

## 8. 结论

Vibe2Spec 当前已经完成一个可运行的课程项目原型：它把 Codex 从直接对话式开发推进到 Spec-first artifact 工作流，并提供完整 harness 与轻量 skill 两种使用方式。实验结果表明，在简单任务中，Direct Codex 可能更高效且功能不输；但在包含隐含业务边界的任务中，Vibe2Spec 能通过需求规则、设计决策、验收 fixture 和探针验证显著降低规则遗漏风险。

因此，本项目最合理的定位是“Codex 的工程化前置规划和验证层”。它不替代 Codex，也不追求复杂多 Agent 平台化，而是把 AI coding 中最容易被忽略的需求澄清、边界条件、可追踪性和验证闭环显式化。

## 附录：证据索引

- 项目使用说明：[README.md](../README.md)
- 当前项目盘点：[doc/current-project-analysis.md](current-project-analysis.md)
- 完整 demo 项目：[examples/demo-project](../examples/demo-project)
- Todo 对比实验：[experiments/vibe2spec-vs-direct-20260605/REPORT.md](../experiments/vibe2spec-vs-direct-20260605/REPORT.md)
- Sprint Board 对比实验：[experiments/web-harness-vs-direct-20260603/REPORT.md](../experiments/web-harness-vs-direct-20260603/REPORT.md)
- Proration 对比实验：[experiments/proration-vibe2spec-vs-direct-20260605/REPORT.md](../experiments/proration-vibe2spec-vs-direct-20260605/REPORT.md)
- Proration Direct 探针结果：[direct-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/direct-probe-result.json)
- Proration Vibe2Spec 探针结果：[vibe2spec-probe-result.json](../experiments/proration-vibe2spec-vs-direct-20260605/vibe2spec-probe-result.json)
