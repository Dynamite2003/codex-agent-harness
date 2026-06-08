目标：
生成 Vibe Coding 用的 prompt。

输入：
需求文档 doc/proposal.md；详细设计：doc/detailed-design.md；任务划分：doc/tasks。
当前解析到的输入：
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/proposal.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/detailed-design.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer/doc/tasks (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 实现 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
doc/prompt.md。

步骤：
阅读输入信息，了解当前要实现的工程，生成 doc/prompt.md 用来作为轻量 Vibe Coding 起始 prompt。
doc/prompt.md 必须默认采用单 agent 顺序执行：按 doc/tasks/progress.md 推进、实现代码、运行验证、更新 checklist。
只有当任务彼此独立、文件范围清晰、预计单 agent 上下文会明显过长时，doc/prompt.md 才允许可选启用子 agents；不得强制并行或强制开启多个 subagents。
如果启用子 agents，doc/prompt.md 必须要求先声明文件所有权、合并顺序和冲突处理策略。
doc/prompt.md 必须要求实现时遵守 Spec / ADR / Acceptance Criteria；如代码实现偏离 spec，必须回填相关文档或记录偏离原因。
doc/prompt.md 必须要求 agent 根据对应的 doc/tasks/<module-name>.md 实现代码、按项目技术栈补充 focused tests 或等价验证，并把完成状态回写到任务 checklist。
doc/prompt.md 必须要求 agent 先识别现有技术栈和可用工具，再选择验证命令；不要为静态 Web、无依赖项目或已有项目强行引入不存在的 uv、pytest、mypy、ruff、npm、node。
doc/prompt.md 必须要求 Python 项目优先沿用仓库现有测试命令；只有已经 bootstrap-python 或项目已有 uv/pytest/mypy/ruff 配置时，才使用 uv run pytest、uv run mypy、uv run ruff check .。
doc/prompt.md 必须要求静态 Web 或无依赖前端项目至少做契约测试、源码级逻辑测试、DOM smoke 或浏览器截图验证；如果浏览器或运行时不可用，要记录不可用原因和替代验证。
doc/prompt.md 必须要求最终报告包含：完成项、关键文件、验证命令与结果、未验证风险、spec 回填或偏离记录。
生成 prompt 过程中任何不明确的地方需要向我提问，不要猜测我的意图。
