---
name: expand-requirements-prompt
description: Expand a short product idea into a complete Chinese Spec-first requirements prompt for Codex. Use when the user says 需求 prompt, Spec prompt, 需求阶段, PRD, 产品需求, MVP 需求, or wants a lightweight alternative to codex-agent-harness for generating doc/proposal.md with EARS requirements, ADR candidates, acceptance criteria, scope, non-goals, risks, and clarification questions.
---

# Expand Requirements Prompt

## Workflow

Take the user's brief idea and return a single copy-ready prompt in Chinese. Do not run a harness, do not create files, and do not start implementation unless explicitly asked.

If the user did not specify an output path, use `doc/proposal.md`. If the user did not specify a project directory, write the prompt so the receiving agent asks for or infers it from the current workspace.

## Output Shape

Return only the expanded prompt, preferably in a fenced `text` block. Include these sections:

- 目标
- 输入
- 输出
- 步骤
- Spec 规范
- 待确认策略

## Requirements Prompt Template

Use this structure and fill bracketed items from the user's idea:

```text
你是一个资深产品经理和软件需求分析师。现在只完成需求阶段，不做技术设计、任务拆分或代码实现。

目标：
用户的原始想法是：[粘贴用户的一句话/简单 prompt]
请把它扩展为一个真实可开发的 MVP Spec-first 需求文档，重点澄清产品目标、用户、边界、功能、关键决策、验收标准、风险和待确认问题。

输入：
- 当前项目目录：[如已知则填写；未知则要求读取当前工作区]
- 现有资料：[列出用户提供的文档/链接/代码；没有则写“无”]
- 约束：[例如 Web 端、移动端、中文市场、低成本 MVP、不能调用付费 API 等]

输出：
请生成或更新 doc/proposal.md。
文档必须包含：
1. Context
2. Goals & Non-Goals
3. 目标用户
4. User Stories
5. Functional Requirements (EARS)
6. Key Decisions / ADR Candidates
7. Acceptance Criteria (GIVEN-WHEN-THEN)
8. Out of Scope
9. 数据、内容或外部依赖
10. 权限、隐私、安全、合规约束
11. 关键风险和缓解策略
12. Open Questions

如果需求属于新 feature、跨模块改动、新 schema/API/agent、或架构级重构，请同时创建或更新 doc/specs/index.md 和 doc/specs/YYYY-MM-DD-topic.md；如果不需要独立 spec，请在 doc/proposal.md 中说明理由。

步骤：
1. 先阅读项目目录和用户提供的资料，判断是否依赖现有系统。
2. 将用户的简单想法拆成可执行的 MVP 范围，避免一次性规划过大。
3. 明确哪些能力进入首版，哪些放到后续版本。
4. 将核心功能需求写成 EARS 原子语句：WHEN / WHILE / IF...ELSE + THE SYSTEM SHALL。
5. 将关键产品或技术决策记录为 ADR Candidates，至少包含 Decision、Why、Alternatives。
6. 将可验收行为写成 GIVEN-WHEN-THEN，并确保每条都可手测或自动化验证。
7. 对影响设计阶段的关键不明确点，写入 Open Questions；如果问题阻塞需求成稿，先向用户提问。
8. 不要写架构设计、数据库设计、接口设计、任务清单或业务代码。

Spec 规范：
- WHY 比 WHAT 重要；关键决策必须说明原因和取舍。
- Non-Goals 和 Out of Scope 必写，避免 scope creep。
- 所有假设必须显式标注为“建议假设”或“待确认”。
- 验收标准必须可观察、可验证。

质量要求：
- 需求必须具体到后续可以直接进入设计阶段。
- 不要把外部信息、日期、政策、价格或比赛考试安排编造成事实；需要最新事实时要求联网核验。
- 语言使用简洁中文，面向真实开发团队。
```
