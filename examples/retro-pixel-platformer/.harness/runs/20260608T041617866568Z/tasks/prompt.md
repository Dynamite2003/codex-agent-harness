目标：
为每一个模块划分最小可执行的任务。

输入：
需求文档：doc/proposal.md；设计文档：doc/detailed-design.md。
当前解析到的输入文档：
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/proposal.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/detailed-design.md (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 任务 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
任务列表：
- doc/tasks/<module-name>.md（每一个模块对应一个）。
- doc/tasks/progress.md（总体进度）。
每个任务文件必须包含：模块目标、依赖输入、Out of Scope、任务 checklist、验收标准、测试要求、AFK/HITL 标记、Blocked by、可能修改的文件范围。

步骤：
根据需求文档和详细设计，为每一个模块生成最小可执行、可验证任务。
优先按端到端垂直切片拆分，而不是只按技术层拆分。
每一个模块对应一个 <module-name>.md，用 checklist 表示子任务是否完成。
在 progress.md 中用 checklist 表示模块是否完成。
每个任务必须能追溯到 EARS 需求、ADR 或 Acceptance Criteria。
用 AFK 标记可由 agent 独立完成的任务；用 HITL 标记需要人工确认、密钥、外部账号、产品决策或高风险操作的任务。
任何会影响任务划分的不明确点必须向用户询问，不要猜测我的意图。
不要修改业务代码。
