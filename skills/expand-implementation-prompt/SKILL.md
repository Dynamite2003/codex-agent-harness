---
name: expand-implementation-prompt
description: Expand planning artifacts into a complete Chinese lightweight implementation prompt for Codex. Use when the user says 实现 prompt, 开发 prompt, vibe coding prompt, 编码执行, or wants a prompt that tells Codex to read Spec-first planning docs, implement mostly as a single agent, update checklists, run tests, and report verification without using codex-agent-harness.
---

# Expand Implementation Prompt

## Workflow

Take the user's planning artifacts or project goal and return one copy-ready implementation prompt in Chinese. This skill generates the prompt only; do not start coding unless the user explicitly asks to execute it now.

Default inputs are `doc/proposal.md`, `doc/detailed-design.md`, and `doc/tasks/`. Default final prompt path, when requested, is `doc/prompt.md`.

## Output Shape

Return only the expanded prompt, preferably in a fenced `text` block. Include these sections:

- 目标
- 输入
- 执行规则
- 实现步骤
- 测试与验证
- 进度更新
- 最终交付

## Implementation Prompt Template

```text
你是一个资深全栈工程师。请基于现有规划文档完成项目实现，直到功能可运行、测试通过、任务清单更新。

目标：
实现 [项目名称或用户目标] 的 MVP。

输入：
- 需求文档：[默认 doc/proposal.md]
- 详细设计文档：[默认 doc/detailed-design.md]
- 任务目录：[默认 doc/tasks/]
- 总体进度：[默认 doc/tasks/progress.md]
- 当前项目目录：[如已知则填写；未知则使用当前工作区]

执行规则：
1. 先阅读需求、设计和任务文件，再检查现有代码结构。
2. 优先沿用现有技术栈、目录结构、样式系统和测试方式。
3. 不要回滚用户已有改动；遇到无关脏文件保持不动。
4. 严格按任务 checklist 推进，每完成一项就更新对应任务文件和 progress.md。
5. 对任务中的不明确点，能从需求/设计推断的采用保守 MVP 实现；会影响数据安全、费用、外部服务或产品承诺的先向用户提问。
6. 不要引入无必要的大型框架或复杂抽象。
7. 默认单 agent 顺序执行。只有当任务彼此独立、文件范围清晰、上下文会明显过长时，才可以选择性使用子 agents；不要为了形式强行并行。
8. 实现必须遵守 Spec / ADR / Acceptance Criteria；如果实现偏离文档，必须回填相关文档或记录偏离原因。

实现步骤：
1. 建立或修正项目基础结构、配置和运行脚本。
2. 实现数据模型、核心业务逻辑和服务接口。
3. 实现前端页面、组件、状态、表单、空状态、加载状态和错误状态。
4. 实现外部集成或 mock/stub，并清楚标注真实接入所需环境变量。
5. 实现权限、隐私、安全、审计、免责声明或风险提示等设计要求。
6. 补充必要的单元测试、集成测试或端到端验证。
7. 运行格式化、lint、类型检查和测试；根据项目实际工具选择命令。
8. 如修改了关键行为、schema、API 或跨模块契约，回填 doc/proposal.md、doc/detailed-design.md 或 doc/specs/ 中相关内容。

测试与验证：
- 如果是 Python 项目，优先运行：uv run pytest、uv run mypy、uv run ruff check .
- 如果是 Node/前端项目，优先读取 package.json 并运行对应的 test、lint、typecheck、build。
- 如果需要启动 Web 应用，启动本地开发服务器并给出 URL。
- 对 UI 项目，尽量用浏览器或截图验证关键页面没有空白、错位、文字溢出或明显交互错误。

进度更新：
- 每完成一个模块，更新 doc/tasks/<module-name>.md。
- 每完成一个模块，更新 doc/tasks/progress.md。
- 如果某项无法完成，标记为阻塞并写明原因、已尝试方案和需要用户提供的信息。

最终交付：
请最终说明：
1. 完成了哪些模块
2. 修改了哪些关键文件
3. 运行了哪些验证命令及结果
4. 仍然存在的风险或未完成项
5. 本地运行方式
6. Spec 回填或实现偏离记录
```
