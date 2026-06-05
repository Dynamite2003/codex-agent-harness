目标：
为每一个模块划分最小可执行的任务。

输入：
需求文档：doc/proposal.md；设计文档：doc/detailed-design.md。
当前解析到的输入文档：
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/proposal.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/detailed-design.md (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 任务 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
任务列表：
- doc/tasks/<module-name>.md（每一个模块对应一个）。
- doc/tasks/progress.md（总体进度）。

步骤：
根据需求文档和详细设计，为每一个模块生成 vibe coding 的最小任务。
每一个模块对应一个 <module-name>.md，用 checklist 表示子任务是否完成。
在 progress.md 中用 checklist 表示模块是否完成。
任何会影响任务划分的不明确点必须向用户询问，不要猜测我的意图。
不要修改业务代码。
