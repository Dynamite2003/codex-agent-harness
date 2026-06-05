目标：
生成 Vibe Coding 用的 prompt。

输入：
需求文档 doc/proposal.md；详细设计：doc/detailed-design.md；任务划分：doc/tasks。
当前解析到的输入：
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/proposal.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/detailed-design.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 实现 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
doc/prompt.md。

步骤：
阅读输入信息，了解当前要实现的工程，生成 doc/prompt.md 用来作为 Vibe Coding 的起始 prompt。
doc/prompt.md 必须指定主 agent 作为监督 Agent 跟踪整体进度，读取并维护 doc/tasks/progress.md。
doc/prompt.md 必须要求主 agent 根据 progress.md 自动拉起多个子 agents，每个子 agent 负责一个模块或一个明确的最小任务，避免单个 agent 上下文过长。
doc/prompt.md 必须要求子 agents 根据对应的 doc/tasks/<module-name>.md 实现代码、补充 pytest 单元测试，并把完成状态回写到任务 checklist。
doc/prompt.md 必须要求整个实现过程没有人工参与；监督 Agent 负责分配任务、合并结果、处理失败、重跑验证并更新 progress.md。
doc/prompt.md 必须要求代码有完整的 pytest 单元测试，并通过 mypy 和 ruff 检查；Python 项目优先使用 uv run pytest、uv run mypy、uv run ruff check .。
生成 prompt 过程中任何不明确的地方需要向我提问，不要猜测我的意图。
