---
name: expand-design-prompt
description: Expand a requirements document or short product requirement into a complete Chinese design-stage prompt for Codex. Use when the user says 设计 prompt, 设计阶段, 详细设计, 架构设计, or wants a lightweight prompt that asks Codex to generate doc/detailed-design.md with modules, data model, APIs, workflows, UI states, risks, and test strategy without running codex-agent-harness.
---

# Expand Design Prompt

## Workflow

Take the user's requirement summary or `doc/proposal.md` path and return a single copy-ready prompt in Chinese. Do not generate the design itself unless explicitly asked; generate the prompt that will produce the design.

If no requirements path is given, default to `doc/proposal.md`. If no output path is given, default to `doc/detailed-design.md`.

## Output Shape

Return only the expanded prompt, preferably in a fenced `text` block. Include these sections:

- 目标
- 输入
- 输出
- 步骤
- 设计范围
- 质量要求

## Design Prompt Template

```text
你是一个资深软件架构师和产品型工程师。现在只完成设计阶段，不做任务拆分或代码实现。

目标：
基于需求文档 [默认 doc/proposal.md]，生成可指导开发的详细设计文档。

输入：
- 需求文档：[doc/proposal.md 或用户指定路径]
- 当前项目目录：[如已知则填写；未知则读取当前工作区]
- 现有技术栈或约束：[如 React/Next.js/Python/Node/Postgres；未知则先读取项目再建议]

输出：
请生成或更新 doc/detailed-design.md。
文档必须包含：
1. 设计目标和范围
2. 非目标
3. 系统上下文和主要用户流程
4. 模块划分与职责
5. 模块间依赖关系
6. 数据模型和核心实体
7. API 或服务接口设计
8. 前端页面、组件、状态和交互设计
9. 后台任务、队列、定时任务或外部集成
10. 权限、隐私、安全、合规和审计设计
11. 错误处理、空状态、加载状态和降级策略
12. 测试策略
13. 风险、取舍和待确认问题

步骤：
1. 读取需求文档和项目目录，确认是否已有技术栈和架构约定。
2. 优先沿用现有项目结构和技术选型；如果是空项目，给出保守、易实现的 MVP 设计。
3. 将需求拆成清晰模块，说明每个模块的输入、输出、状态和边界。
4. 对涉及 AI、外部搜索、提醒、支付、日历、邮件、权限等能力，明确失败模式和降级策略。
5. 对不明确但不阻塞设计的点，记录为待确认；对阻塞设计的点，先向用户提问。
6. 不要生成任务 checklist，不要修改业务代码。

质量要求：
- 设计要足够具体，后续可以直接拆任务。
- 避免过度工程化；MVP 优先简单、可验证、可迭代。
- 明确数据来源、可信度、人工校验、审计或合规相关边界。
- 不要臆造外部事实；需要最新政策、考试、比赛、价格或 API 细节时要求联网核验。
```
