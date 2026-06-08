---
name: expand-design-prompt
description: Expand a requirements document or short product requirement into a complete Chinese Spec-first design-stage prompt for Codex. Use when the user says 设计 prompt, 设计阶段, 详细设计, 架构设计, ADR, or wants a lightweight prompt that asks Codex to generate doc/detailed-design.md with modules, data model, API contracts, ADRs, acceptance-criteria mapping, risks, and test strategy without running codex-agent-harness.
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
4. Success Contract 的设计响应：Primary Success Mode、Priority Budget、Non-negotiable Quality Bar、MVP Success Evidence
5. Primary Value Slice：最小端到端成功证明及其用户可见证据
6. 模块划分与职责
7. 模块间依赖关系
8. 数据模型和核心实体
9. API 或服务接口设计
10. 前端页面、组件、状态和交互设计
11. 后台任务、队列、定时任务或外部集成
12. Success Mode、Domain Lenses 和 Failure Modes 的设计响应
13. Behavioral / Quality Requirements 的设计方案
14. 数据/状态不变量、UI 状态矩阵、AI/Agent 行为边界、集成降级策略（仅在适用时）
15. 权限、隐私、安全、合规和审计设计
16. 错误处理、空状态、加载状态、部分成功和恢复策略
17. Key Design Decisions (ADR)
18. Acceptance Criteria 映射
19. 验证策略
20. 风险、取舍和待确认问题

步骤：
1. 读取需求文档和项目目录，确认是否已有技术栈和架构约定。
2. 优先沿用现有项目结构和技术选型；如果是空项目，给出简单、可验证、能证明 Primary Success Mode 的 MVP 设计，不要把“保守”理解为牺牲核心价值。
3. 读取需求中的 Success Contract、Product Archetype、Success Mode、Domain Lenses、Failure Modes、Functional/Behavioral/Quality Acceptance Criteria；如果缺失，补充保守推断并标记为设计假设。
4. 先设计 Primary Value Slice：一个最小端到端用户流程，必须能展示 Primary Success Mode。说明用户看到什么、做什么、得到什么、用什么证据判断成功。
5. 给出 Priority Budget 的设计分配：哪些模块/体验/质量工作消耗主要实现资源，哪些是支持性工作，哪些可以后置。
6. 将需求拆成清晰模块，说明每个模块的输入、输出、状态和边界。
7. 明确每个高风险 Failure Mode 由哪个模块、状态、流程、约束或验证方式覆盖。
8. 对 UI 项目输出页面/组件状态矩阵；对数据/工作流项目输出状态机、不变量和权限矩阵；对 AI/Agent 项目输出工具边界、记忆/隐私、拒答/升级和 eval 集；对集成项目输出超时、重试、幂等、降级和契约测试；对原型项目输出学习目标和可丢弃边界。
9. 把需求阶段的 ADR Candidates 收敛为明确 ADR；每条 ADR 必须包含 Decision、Why、Alternatives / Tradeoffs。
10. 将 EARS 需求和 Functional / Behavioral / Quality Acceptance Criteria 映射到模块、接口、UI 状态或测试策略。
11. 对涉及 AI、外部搜索、提醒、支付、日历、邮件、权限等能力，明确失败模式和降级策略。
12. 如果设计会改变既有关键行为或已有 spec，列出需要回填的 spec 文件。
13. 对不明确但不阻塞设计的点，记录为待确认；对阻塞设计的点，先向用户提问。
14. 不要生成任务 checklist，不要修改业务代码。

质量要求：
- 设计要足够具体，后续可以直接拆任务。
- 避免过度工程化；MVP 优先简单、可验证、可迭代。
- MVP 是最小成功证明，不是最小功能集合；如果某个设计无法观察 Primary Success Mode，应扩大或重排 MVP，而不是把成功推迟到后续。
- 不要只设计“功能存在”；必须设计如何满足 Success Mode、Quality Requirements 和主要 Failure Modes。
- Primary Success Mode 不能只落到 HITL。对需要人工判断的质量，必须设计 AFK proxy metric、demo artifact、可观察用户流程或可回放证据。
- 对体验型、创意型、工具型或消费型产品，必须设计反馈、状态、可理解性和质量调优路径；对正确性/合规型产品，必须设计不变量、审计、权限和失败恢复。
- WHY 比 WHAT 重要；不要只描述“做什么”，必须解释关键设计为什么这样做。
- 明确数据来源、可信度、人工校验、审计或合规相关边界。
- 不要臆造外部事实；需要最新政策、考试、比赛、价格或 API 细节时要求联网核验。
```
