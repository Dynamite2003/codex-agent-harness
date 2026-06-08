---
name: expand-requirements-prompt
description: Expand a short product idea into a complete Chinese Spec-first requirements prompt for Codex. Use when the user says 需求 prompt, Spec prompt, 需求阶段, PRD, 产品需求, MVP 需求, or wants a lightweight alternative to codex-agent-harness for generating doc/proposal.md with Success Contract, EARS requirements, ADR candidates, acceptance criteria, scope, non-goals, risks, and clarification questions.
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
3. Success Contract：Primary Success Mode、Priority Budget、Non-negotiable Quality Bar、MVP Success Evidence
4. 目标用户
5. User Stories
6. Functional Requirements (EARS)
7. Key Decisions / ADR Candidates
8. Acceptance Criteria (GIVEN-WHEN-THEN)
9. Out of Scope
10. Product Archetype / Success Mode / Domain Lenses
11. Failure Mode Lens
12. Behavioral Requirements
13. Quality Requirements
14. 数据、状态、内容或外部依赖
15. UI / AI / 数据 / 集成等场景化要求（仅在适用时）
16. 权限、隐私、安全、合规约束
17. Verification Strategy
18. 关键风险和缓解策略
19. Open Questions

如果需求属于新 feature、跨模块改动、新 schema/API/agent、或架构级重构，请同时创建或更新 doc/specs/index.md 和 doc/specs/YYYY-MM-DD-topic.md；如果不需要独立 spec，请在 doc/proposal.md 中说明理由。

步骤：
1. 先阅读项目目录和用户提供的资料，判断是否依赖现有系统。
2. 将用户的简单想法拆成可执行的 MVP 范围，避免一次性规划过大。
3. 识别目标用户、使用上下文和 Product Archetype，可多选：CRUD/Admin、Workflow/Approval、Dashboard/Analytics、Search/Discovery、Editor/Builder、Consumer App、Creative Experience、Game/Simulation、AI Assistant/Agent、Automation/Script、Data Pipeline、API/SDK/CLI、Integration/Connector、Migration/Refactor、Infrastructure/DevOps、Security/Compliance、Prototype/Spike。
4. 识别 Success Mode，可多选并说明优先级：Correctness、Usability、Experience、Reliability、Throughput、Exploration、Compliance/Safety。
5. 写出 Success Contract：
   - Primary Success Mode：只能选一个最高优先级；其他 Success Mode 排序说明。
   - Priority Budget：用百分比或明确顺序说明实现和验收资源如何分配，避免最高目标被 checklist 稀释。
   - Non-negotiable Quality Bar：如果达不到，功能完成也不能算成功。
   - MVP Success Evidence：MVP 必须展示什么可观察证据来证明 Primary Success Mode，不能只写“待人工确认”。
6. 选择 Domain Lenses：Workflow、Data、Interface、Creative、Automation、Integration、AI/Agent、Security/Compliance、Migration、Operations。
7. 识别最可能失败的 Failure Modes：结果错误、流程混乱、边界状态缺失、性能差、数据丢失、权限泄漏、不可逆操作、失败后无法恢复、视觉/交互质量低、集成漂移、AI 幻觉或越权、架构难维护。
8. 明确哪些能力进入首版，哪些放到后续版本；MVP 是“最小成功证明”，不是“最少功能集合”。如果砍掉某项会让 Primary Success Mode 不可观察，则不能砍。
9. 将核心功能需求写成 EARS 原子语句：WHEN / WHILE / IF...ELSE + THE SYSTEM SHALL。
10. 补充 Behavioral Requirements：正常、边界、失败、恢复、空/加载/部分成功、权限不足等状态下系统如何表现。
11. 补充 Quality Requirements：任务清晰度、交互质量、反馈质量、错误处理、性能、数据正确性、可维护性、视觉质量、可访问性中适用的维度；不要只写“体验好”，要写可观察标准。
12. 对适用场景补充专项要求：
   - UI：default/loading/empty/error/partial success/disabled/permission denied/confirmation/recovery states。
   - AI/Agent：允许/禁止动作、工具边界、引用来源、不确定性表达、拒答/升级、记忆和隐私、评测样例。
   - Data/State：必填字段、唯一性、状态转换、幂等、一致性、保留/删除、审计。
   - Integration：认证、速率限制、超时、重试、降级、契约漂移。
   - Exploration：学习目标、待验证假设、一次性原型 vs 可复用部分，避免过早架构化。
13. 将关键产品或技术决策记录为 ADR Candidates，至少包含 Decision、Why、Alternatives。
14. 将验收标准分为 Functional / Behavioral / Quality Acceptance Criteria，并使用 GIVEN-WHEN-THEN；确保每条都可手测、自动化验证或明确 HITL 审查。
15. 为 Primary Success Mode 至少写 3 条 AFK 可验证或可演示的 Acceptance Criteria。HITL 可以确认质量，但不能成为 Primary Success Mode 的唯一证据。
16. 定义 Verification Strategy：单元、集成、契约、UI 状态、权限矩阵、迁移 dry-run、性能预算、可访问性、视觉截图、AI eval/replay、人工创意/法律/品牌审查中适用的检查。
17. 对影响设计阶段的关键不明确点，写入 Open Questions；如果问题阻塞需求成稿，先向用户提问。
18. 不要写架构设计、数据库设计、接口设计、任务清单或业务代码。

Spec 规范：
- WHY 比 WHAT 重要；关键决策必须说明原因和取舍。
- Spec 不是功能清单。必须说明本项目“怎样才算成功”，并覆盖该场景最可能失败的地方。
- Success Contract 是最高优先级约束。后续设计、任务和实现必须优先证明 Primary Success Mode；不能让它被模块 checklist、合规记录或测试基础设施稀释。
- Acceptance Criteria 必须分层：Functional Acceptance、Behavioral Acceptance、Quality Acceptance。
- Anti-Checklist Rule：功能存在不代表验收通过；如果实现技术上可用但不满足 Success Mode 和 Quality Requirements，必须标记为未完成或待调优。
- HITL Rule：人工确认可以阻塞发布，但不能替代 MVP 对 Primary Success Mode 的可观察证据；必须提供 AFK proxy metric、demo artifact 或用户流程证据。
- Non-Goals 和 Out of Scope 必写，避免 scope creep。
- 所有假设必须显式标注为“建议假设”或“待确认”。
- 验收标准必须可观察、可验证。

质量要求：
- 需求必须具体到后续可以直接进入设计阶段。
- 不要把外部信息、日期、政策、价格或比赛考试安排编造成事实；需要最新事实时要求联网核验。
- 语言使用简洁中文，面向真实开发团队。
```
