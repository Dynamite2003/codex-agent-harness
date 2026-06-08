目标：
根据需求文档生成详细设计文档。

输入：
需求文档 doc/proposal.md。
当前解析到的需求文档：
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/proposal.md (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 设计 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
设计文档 doc/detailed-design.md。
设计文档必须包含：Context、Goals & Non-Goals、模块划分、数据模型、状态机或关键流程、API / 本地契约、Key Design Decisions (ADR)、Acceptance Criteria 映射、风险和测试策略。

步骤：
根据需求文档的内容，划分出模块，识别模块之间的关系，生成详细设计文档。
把需求阶段的 ADR Candidates 收敛为明确 ADR；每条 ADR 必须说明 Decision、Why、Alternatives / Tradeoffs。
如果实现会改变既有关键行为或已有 spec，必须在设计文档中列出需要回填的 spec 文件。
验收标准必须能映射到后续任务和测试，不要只写泛化的“功能正常”。
不要猜测我的意图，任何不明确的地方向我询问。
不要生成任务清单或修改业务代码。
