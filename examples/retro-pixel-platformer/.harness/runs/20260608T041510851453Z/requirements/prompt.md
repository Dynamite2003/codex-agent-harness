目标：
用户的具体需求是：创作一款原创复古像素横版平台跳跃游戏，玩法灵感来自经典平台游戏：玩家控制原创角色在关卡中奔跑、跳跃、收集物品、躲避或踩踏敌人，并到达终点。要求浏览器可运行、像素美术风格、键盘操作、至少一个可玩关卡、计分/生命/胜负状态、不要使用超级马里奥、任天堂角色、名称、素材、关卡布局或可识别的商业 IP。当前阶段只生成 Vibe2Spec 规划 artifacts 和最终实现 prompt，不开始实际编码。
现在只完成需求阶段，目标是生成清晰、可确认、可进入设计阶段的需求文档。

输入：
当前项目目录：/Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer
全局约束：
- 如果目标项目以 Python 为主要语言，进入 harness 前必须先通过 codex-harness bootstrap-python 准备 uv 隔离环境，并配置 ruff、mypy、pytest。
- 默认采用 Spec-first 工作流：先把需求、边界、关键决策和验收标准写成可审阅 artifact，再进入设计、任务或实现。
- Spec 中必须重视 WHY：关键决策要用 ADR 记录原因、替代方案和权衡；功能需求优先使用 EARS，验收标准优先使用 GIVEN-WHEN-THEN。
- 只执行当前阶段，不要提前进入后续阶段。
- 每个阶段都视为新的独立对话；不要依赖其他阶段的聊天历史，只能通过明确声明的文档 artifact 传递上下文。
- 不要揣测用户意图；任何关键不明确点必须向用户提问。
- 如果当前阶段需要用户回答才能继续，不要进入下一阶段所需的实质输出；最终回复必须包含独占一行的 HARNESS_NEEDS_USER_INPUT，并在其后列出需要用户回答的问题。harness 检测到该标记后会停止，不会继续后续阶段。
- 只修改当前阶段输出要求中声明的文件。
- 不要回滚用户已有改动。
上游 artifact：
- 无上游 artifact
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 需求 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
请在 doc/proposal.md 生成 Spec-first 需求文档。
文档必须包含：Context、Goals & Non-Goals、User Stories、Functional Requirements (EARS)、Key Decisions / ADR Candidates、Acceptance Criteria (GIVEN-WHEN-THEN)、Out of Scope、Constraints、Open Questions。
如果本次需求属于新 feature、跨模块改动、新 schema/API/agent、或架构级重构，请同时创建或更新 doc/specs/index.md 和 doc/specs/YYYY-MM-DD-topic.md；如果不需要独立 spec，请在 doc/proposal.md 说明理由。

步骤：
先阅读项目目录和必要文件，判断需求是否依赖现有系统。
明确哪些内容是用户已确认事实，哪些只是建议假设；不要把建议假设写成事实。
将核心功能需求写成 EARS 原子语句，例如 WHEN <触发条件> THE SYSTEM SHALL <行为>。
将关键产品或技术决策记录为 ADR Candidates，至少包含 Decision、Why、Alternatives。
将可验收行为写成 GIVEN-WHEN-THEN，并确保每条都可手测或自动化验证。
使用提问的方式确认不明确的需求；不要替用户补全关键决策。
如果信息足够，生成 proposal.md；如果信息不足，proposal.md 中必须列出阻塞问题和推荐的下一轮提问。
不要做设计、任务拆分或代码实现。
