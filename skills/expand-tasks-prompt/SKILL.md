---
name: expand-tasks-prompt
description: Expand requirements and design artifacts into a complete Chinese task-breakdown prompt for Codex. Use when the user says 任务 prompt, 任务拆分, task breakdown, progress.md, or wants Codex to create doc/tasks/progress.md and per-module task checklists from doc/proposal.md and doc/detailed-design.md without running a full harness.
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
- doc/tasks/<module-name>.md：每个模块一个任务文件

每个模块任务文件必须包含：
1. 模块目标
2. 依赖输入
3. 不做什么
4. 任务 checklist
5. 验收标准
6. 测试要求
7. 风险和注意事项

步骤：
1. 阅读需求和设计文档，识别模块边界、依赖关系和可并行工作。
2. 为每个模块创建一个清晰的任务文件，文件名使用英文小写短横线。
3. 将任务拆到 0.5-2 小时内可完成的粒度；每个任务必须有明确产出。
4. 在 progress.md 中列出模块总览、推荐执行顺序、可并行项和阻塞项。
5. 对跨模块依赖、数据库迁移、外部服务、环境变量、测试数据和验收方式单独列明。
6. 如发现需求或设计存在阻塞矛盾，先向用户提问；否则记录为待确认并继续拆分。
7. 不要修改业务代码，不要安装依赖，不要启动服务。

任务粒度规则：
- 每个 checklist 项必须以动词开头，例如“实现...”“补充...”“验证...”。
- 每个任务必须能被测试或人工验收。
- 不要写“优化体验”“完善功能”这类不可验收任务，除非拆成具体行为。
- 优先把基础设施、数据模型、核心流程、测试、错误状态和文档分开。

质量要求：
- 任务清单要能直接交给实现 agent 执行。
- 覆盖前端、后端、数据、外部集成、权限、安全、测试和发布验证。
- 保持 MVP 范围，不引入设计文档未要求的大功能。
```
