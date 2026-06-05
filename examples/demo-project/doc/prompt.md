# Demo Implementation Prompt

目标：
基于 `doc/proposal.md`、`doc/detailed-design.md` 和 `doc/tasks/` 实现 Todo deadline MVP。

输入：

- `doc/proposal.md`
- `doc/detailed-design.md`
- `doc/tasks/progress.md`
- `doc/tasks/deadline-todo.md`

执行规则：

1. 默认单 agent 顺序执行；subagents 只是可选策略，本 demo 不启用。
2. 遵守 Spec / ADR / Acceptance Criteria。
3. 修改完成后更新任务 checklist。
4. 运行浏览器或源码级验证；记录验证结果。

最终交付：

- 完成项。
- 关键文件。
- 验证命令与结果。
- Spec 回填或实现偏离记录。
