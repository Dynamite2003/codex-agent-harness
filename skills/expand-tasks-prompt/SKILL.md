---
name: expand-tasks-prompt
description: Expand requirements and design artifacts into a complete Chinese Spec-traceable task-breakdown prompt for Codex. Use when the user says 任务 prompt, 任务拆分, task breakdown, progress.md, AFK/HITL, or wants Codex to create doc/tasks/progress.md and per-module task checklists from doc/proposal.md and doc/detailed-design.md without running a full harness.
---

# Expand Tasks Prompt

## Workflow

Take the user's planning artifacts or short description and return one copy-ready prompt in Chinese for generating implementation task files. Do not implement code.

Default inputs are `doc/proposal.md` and `doc/detailed-design.md`. Default outputs are `doc/tasks/progress.md` and `doc/tasks/<module-name>.md`.

## Output Shape

Return only the expanded prompt, preferably in a fenced `text` block. Include these sections:

- 目标
- 输入
- 输出
- 步骤
- 任务粒度规则
- 质量要求

## Tasks Prompt Template

```text
你是一个资深技术负责人。现在只完成任务拆分阶段，不写业务代码。

目标：
基于需求文档和详细设计，将项目拆成最小可执行、可验证、适合逐步实现的任务清单。

输入：
- 需求文档：[默认 doc/proposal.md]
- 详细设计文档：[默认 doc/detailed-design.md]
- 当前项目目录：[如已知则填写；未知则读取当前工作区]

输出：
请生成或更新：
- doc/tasks/progress.md：总体模块进度 checklist
- doc/tasks/primary-value-slice.md：最高优先级成功证明的端到端切片任务
- doc/tasks/<module-name>.md：每个模块一个任务文件

每个模块任务文件必须包含：
1. 模块目标
2. 依赖输入
3. 不做什么
4. 任务 checklist
5. 追溯关系：对应 EARS / ADR / Acceptance Criteria
6. 验收标准
7. 测试要求
8. AFK/HITL 标记
9. Blocked by
10. 可能修改的文件范围
11. 风险和注意事项
12. Success Mode / Failure Mode / Quality Trace

步骤：
1. 阅读需求和设计文档，识别 Success Contract、Primary Success Mode、Priority Budget、Primary Value Slice、模块边界、依赖关系、Domain Lenses、Failure Modes、验收标准和可并行工作。
2. 先创建 `doc/tasks/primary-value-slice.md`。它必须描述最小端到端用户可见成功证明、AFK 可完成证据、验证方式、HITL 只确认不替代的事项。
3. 在 progress.md 的推荐执行顺序中，把 `primary-value-slice.md` 放在第一位；模块基础设施只能前置到“切片运行所必需”的程度。
4. 为每个模块创建一个清晰的任务文件，文件名使用英文小写短横线。
5. 将任务拆到 0.5-2 小时内可完成的粒度；每个任务必须有明确产出。
6. 在 progress.md 中列出模块总览、推荐执行顺序、可并行项和阻塞项，并标明哪些任务属于 Primary Success Mode 预算。
7. 每个任务必须能追溯到 EARS 需求、ADR、Functional/Behavioral/Quality Acceptance Criteria、Failure Mode、Quality Requirement 或 Success Contract；无法追溯的任务要说明为什么必要。
8. 任务集合必须包含：Primary Value Slice、核心功能实现、边界/失败状态实现、质量 pass、验证 pass。不要只拆“功能模块”。
9. 按场景补充专门任务：UI 状态覆盖、权限矩阵、数据不变量、迁移 dry-run、集成契约、AI eval/replay、性能预算、可访问性、视觉截图或人工品牌/法律/创意审查。
10. 用 AFK 标记可由 agent 独立完成的任务；用 HITL 标记需要人工确认、密钥、外部账号、产品决策、创意/法律/品牌判断或高风险操作的任务。
11. 对 Primary Success Mode 相关的 HITL 项，必须同时给出 AFK proxy metric、demo artifact 或可观察证据任务；不得只写“待人工确认”。
12. 对跨模块依赖、数据库迁移、外部服务、环境变量、测试数据和验收方式单独列明。
13. 如发现需求或设计存在阻塞矛盾，先向用户提问；否则记录为待确认并继续拆分。
14. 不要修改业务代码，不要安装依赖，不要启动服务。

任务粒度规则：
- 每个 checklist 项必须以动词开头，例如“实现...”“补充...”“验证...”。
- 每个任务必须能被测试或人工验收。
- 不要写“优化体验”“完善功能”这类不可验收任务，除非拆成具体行为。
- 优先 Primary Value Slice，其次才是基础设施、数据模型、核心流程、测试、错误状态和文档分开。
- 优先垂直切片，保证每个切片有端到端可观察结果；只有基础设施或共享模块才按技术层拆分。
- 对最高优先级成功标准，至少拆出 3 个 AFK 可完成 checklist 项；这些项必须产生用户可见或可回放证据。
- 对体验/创意/消费类产品，必须拆出反馈、可理解性、视觉/交互质量和调优验证任务。
- 对正确性/可靠性/合规类产品，必须拆出边界条件、不变量、权限/审计、失败恢复和回归验证任务。
- 对探索原型，任务应围绕学习目标和假设验证，避免提前拆出沉重基础设施。

质量要求：
- 任务清单要能直接交给实现 agent 执行。
- 覆盖前端、后端、数据、外部集成、权限、安全、测试和发布验证。
- 保持 MVP 范围，但 MVP 必须证明 Primary Success Mode；不能为了“最小”而让最高成功标准不可观察。
- 不接受“所有功能勾完但 Success Mode 未满足”的任务拆分；必须有质量验收或调优闭环。
- 不接受把 Primary Success Mode 完全标为 HITL；HITL 可以阻塞发布，但不能替代实现阶段的成功证据。
```
