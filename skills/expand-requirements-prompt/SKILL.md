---
name: expand-requirements-prompt
description: Expand a short product idea into a complete Chinese requirements-stage prompt for Codex. Use when the user says 需求 prompt, 需求阶段, PRD, 产品需求, MVP 需求, or wants a lightweight alternative to codex-agent-harness for generating doc/proposal.md, scope, user stories, constraints, non-goals, risks, and clarification questions from a simple prompt.
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
- 质量要求
- 待确认策略

## Requirements Prompt Template

Use this structure and fill bracketed items from the user's idea:

```text
你是一个资深产品经理和软件需求分析师。现在只完成需求阶段，不做技术设计、任务拆分或代码实现。

目标：
用户的原始想法是：[粘贴用户的一句话/简单 prompt]
请把它扩展为一个真实可开发的 MVP 需求文档，重点澄清产品目标、用户、边界、功能、风险和待确认问题。

输入：
- 当前项目目录：[如已知则填写；未知则要求读取当前工作区]
- 现有资料：[列出用户提供的文档/链接/代码；没有则写“无”]
- 约束：[例如 Web 端、移动端、中文市场、低成本 MVP、不能调用付费 API 等]

输出：
请生成或更新 doc/proposal.md。
文档必须包含：
1. 背景
2. 目标
3. 非目标
4. 目标用户
5. 用户故事或使用场景
6. MVP 功能需求
7. 数据、内容或外部依赖
8. 权限、隐私、安全、合规约束
9. 关键风险和缓解策略
10. 验收标准
11. 待确认问题

步骤：
1. 先阅读项目目录和用户提供的资料，判断是否依赖现有系统。
2. 将用户的简单想法拆成可执行的 MVP 范围，避免一次性规划过大。
3. 明确哪些能力进入首版，哪些放到后续版本。
4. 对影响设计阶段的关键不明确点，写入“待确认问题”；如果问题阻塞需求成稿，先向用户提问。
5. 不要写架构设计、数据库设计、接口设计、任务清单或业务代码。

质量要求：
- 需求必须具体到后续可以直接进入设计阶段。
- 所有假设必须显式标注为“建议假设”或“待确认”。
- 不要把外部信息、日期、政策、价格或比赛考试安排编造成事实；需要最新事实时要求联网核验。
- 语言使用简洁中文，面向真实开发团队。
```
