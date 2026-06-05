# Sprint Board Lite 实现阶段 Prompt

## 目标

你是主 agent，也是实现阶段的监督 Agent。基于当前工作区内已经生成的规划 artifact，完成 Sprint Board Lite 的 MVP 实现，直到静态 Web 应用可运行、任务清单更新、测试和检查通过。

项目目标：

- 构建 dependency-free 的静态 Web 应用 Sprint Board Lite。
- 首屏直接呈现可操作的冲刺看板，不做营销页。
- 使用 plain HTML、CSS、JavaScript 实现任务新增、查看、筛选、状态更新、删除、localStorage 持久化、JSON 导出和 JSON 导入。
- 保留并满足现有契约测试约束，不删除、不跳过、不弱化、不重写现有测试。
- 代码必须配套完整的 pytest 单元测试，并通过 mypy 和 ruff 检查；同时保留并运行现有 Python unittest 契约测试。

## 输入

只允许使用本 prompt 明确列出的输入和当前工作区 artifact。不要依赖其他阶段的聊天历史。

- 当前项目目录：`/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow`
- 需求文档：`doc/proposal.md`
- 详细设计文档：`doc/detailed-design.md`
- 任务目录：`doc/tasks/`
- 总体进度：`doc/tasks/progress.md`
- 现有实现文件：
  - `index.html`
  - `src/styles.css`
  - `src/app.js`
- 现有契约测试：
  - `tests/test_static_contract.py`

任务模块文件：

- `doc/tasks/page-structure.md`
- `doc/tasks/data-model.md`
- `doc/tasks/normalization.md`
- `doc/tasks/persistence.md`
- `doc/tasks/metrics.md`
- `doc/tasks/filtering.md`
- `doc/tasks/board-rendering.md`
- `doc/tasks/interactions.md`
- `doc/tasks/json-import-export.md`
- `doc/tasks/styles-responsive.md`
- `doc/tasks/accessibility.md`
- `doc/tasks/verification.md`

## 输出

最终交付必须包括：

- 已实现的静态 Web 应用：
  - `index.html`
  - `src/styles.css`
  - `src/app.js`
- 必要的 focused pytest 单元测试，不替代现有契约测试。
- 已更新的任务 checklist：
  - 每个完成模块对应更新 `doc/tasks/<module-name>.md`
  - 总体进度更新 `doc/tasks/progress.md`
- 验证结果记录：
  - pytest
  - mypy
  - ruff
  - 现有 unittest 契约测试
  - 必要的手动 smoke test
- 最终回复说明完成模块、关键文件、运行命令和结果、剩余风险、本地运行方式。

## 执行规则

1. 主 agent 必须作为监督 Agent 工作，负责读取 `doc/tasks/progress.md`、分配任务、跟踪整体进度、合并结果、处理失败、重跑验证并更新 `progress.md`。
2. 实现过程必须无人工参与。遇到失败时，监督 Agent 自行定位、回滚自己的错误改动、重新分配或重跑验证；只有在 artifact 之间存在无法自行解决的硬冲突时，才在任务文件中标记阻塞并说明原因。
3. 主 agent 必须根据 `doc/tasks/progress.md` 自动拉起多个子 agents。每个子 agent 只负责一个模块，或一个明确的最小任务，避免单个 agent 上下文过长。
4. 子 agents 必须先读取对应的 `doc/tasks/<module-name>.md`，再读取必要的 `doc/proposal.md`、`doc/detailed-design.md` 和相关源码。
5. 子 agents 必须按对应任务文件中的 checklist 实现代码、补充 pytest 单元测试，并把完成状态回写到对应 checklist。
6. 子 agents 不得修改与自己模块无关的文件。跨模块改动必须交给监督 Agent 协调合并。
7. 监督 Agent 必须维护 `doc/tasks/progress.md`：模块开始、完成、阻塞、验证结果和跨模块注意事项都要及时更新。
8. 不要引入后端、数据库、登录、多用户协作、npm、构建工具、前端框架、远程 CDN、外部字体、外部图片或第三方前端资源。
9. 不要删除、跳过、弱化或重写 `tests/test_static_contract.py`。
10. 实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，并在必要时补充 focused tests 和测试配置。任何其他文件改动必须有明确实现或验证必要性。
11. 不要回滚用户已有改动。发现无关脏文件时保持不动；发现相关改动时先理解并在其基础上继续。
12. 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
13. 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
14. KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
15. JSON 导入必须原子替换完整任务列表，不做合并。
16. 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
17. DOM 启动逻辑必须保护非浏览器环境，避免测试加载模块时报错。

## 子 Agent 分工

监督 Agent 按以下顺序调度；可并行项按 `doc/tasks/progress.md` 执行，但合并时必须保证依赖顺序正确。

1. 页面结构子 agent：实现 `doc/tasks/page-structure.md`。
2. 数据模型子 agent：实现 `doc/tasks/data-model.md`。
3. 数据归一化子 agent：实现 `doc/tasks/normalization.md`。
4. 持久化子 agent：实现 `doc/tasks/persistence.md`。
5. 指标计算子 agent：实现 `doc/tasks/metrics.md`。
6. 筛选子 agent：实现 `doc/tasks/filtering.md`。
7. 看板渲染子 agent：实现 `doc/tasks/board-rendering.md`。
8. 交互控制子 agent：实现 `doc/tasks/interactions.md`。
9. JSON 导入导出子 agent：实现 `doc/tasks/json-import-export.md`。
10. 样式和响应式子 agent：实现 `doc/tasks/styles-responsive.md`。
11. 可访问性子 agent：实现 `doc/tasks/accessibility.md`。
12. 验证子 agent：执行 `doc/tasks/verification.md`，补齐验证记录并推动修复。

每个子 agent 的完成条件：

- 对应 checklist 全部完成或明确标记阻塞。
- 相关代码已实现。
- 相关 pytest 单元测试已补充或更新。
- 相关验证已运行，结果写回任务文件。
- 子 agent 向监督 Agent 汇报改动文件、验证命令、失败项和后续依赖。

## 步骤

1. 监督 Agent 读取 `doc/proposal.md`、`doc/detailed-design.md`、`doc/tasks/progress.md` 和所有 `doc/tasks/*.md`。
2. 监督 Agent 检查当前项目结构、现有源码和 `tests/test_static_contract.py`，记录契约测试要求的元素 id、函数名、样式 selector、存储 key 和基础文案。
3. 监督 Agent 根据 `progress.md` 建立执行队列，自动拉起多个子 agents。每个子 agent 的上下文只包含对应模块文档、必要设计片段和相关源码。
4. 页面结构子 agent 先稳定 HTML 骨架，确保首屏包含 header、KPI、表单、筛选器、导入导出控件和四列看板。
5. 数据模型、归一化、指标计算子 agents 在页面骨架稳定后并行实现纯逻辑和 pytest 测试。
6. 持久化、筛选、看板渲染子 agents 基于纯逻辑继续实现 localStorage、筛选和 DOM 渲染。
7. 交互控制和 JSON 导入导出子 agents 实现新增、搜索、筛选、状态变更、删除、导出、导入和反馈。
8. 样式和响应式子 agent 实现密集、实用、可读的 dashboard UI，检查桌面和移动端不出现文字重叠。
9. 可访问性子 agent 检查 label、focus、键盘操作、aria-live、状态和优先级文本表达。
10. 验证子 agent 运行完整测试与检查。失败时把失败原因交回监督 Agent，由监督 Agent 分派给对应子 agent 修复。
11. 监督 Agent 合并所有结果，重新运行完整验证命令，更新每个模块 checklist 和 `doc/tasks/progress.md`。
12. 监督 Agent 输出最终交付说明。

## 实现要点

必须实现并暴露以下 named functions：

- `normalizeTask`
- `calculateMetrics`
- `filterTasks`
- `saveTasks`
- `loadTasks`
- `renderBoard`

核心产品规则：

- 存储 key 固定为 `sprint-board-lite.tasks.v1`。
- 状态值固定为 `backlog`、`doing`、`review`、`done`。
- 优先级固定为 `low`、`medium`、`high`。
- 空标题或纯空白标题不新增、不导入、不从存储恢复到看板。
- 空负责人归一化为 `Unassigned`。
- 无效工作量归一化为 `0`。
- 无效优先级归一化为 `medium`。
- 无效状态归一化为 `backlog`。
- 完成百分比按 `done` 任务数量 / 总任务数量计算，不按工作量加权。
- `localStorage` key 缺失时 seed sample tasks；key 存在为空数组、损坏或无有效任务时不得重新 seed。
- JSON 导入接受任务数组或 `{ "tasks": [...] }`，其他格式报错且不覆盖现有数据。
- JSON 导入成功后替换完整任务列表，不合并。
- 删除任务不需要二次确认。
- 负责人筛选只从当前完整任务列表生成，首项为 `All`。

## 测试与验证

必须优先使用以下命令；如果项目缺少 `uv` 环境，记录原因并使用等价命令，但最终仍要保证 pytest、mypy、ruff 和现有 unittest 契约测试覆盖到位。

```bash
uv run pytest
uv run mypy
uv run ruff check .
python3 -m unittest discover -s tests
```

如果没有现成 pytest 测试，必须补充 focused pytest 单元测试，至少覆盖：

- `normalizeTask` 的有效输入、空标题、空负责人、无效工作量、非法优先级、非法状态、id 保留和 id 生成。
- `calculateMetrics` 的空列表、部分完成、全部完成、高优先级 done 不计入未完成数量、工作量求和。
- `filterTasks` 的关键词搜索、大小写不敏感、状态筛选、负责人筛选和组合筛选。
- `saveTasks` / `loadTasks` 在可 mock 的 localStorage 场景下的 key 缺失、空数组、损坏 JSON 和无效任务过滤。

必须执行手动 smoke test，并在 `doc/tasks/verification.md` 或 `doc/tasks/progress.md` 记录结果：

- 打开页面确认首屏是可操作看板。
- 新增有效任务并确认对应列出现卡片。
- 提交空标题任务并确认不会新增。
- 移动任务到另一个状态并确认 KPI、看板和存储同步更新。
- 删除任务并确认不需要二次确认。
- 使用搜索、状态筛选和负责人筛选定位任务。
- 确认筛选无结果时四列显示 empty state。
- 导出 JSON 并确认文件代表完整任务列表。
- 导入任务数组并确认替换当前任务列表。
- 导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
- 导入非法 JSON 并确认现有任务不变。
- 刷新页面后任务从 `localStorage` 恢复。
- 移动端视口下文本不重叠，表单、筛选器和卡片可操作。
- 所有表单控件有 label，交互控件有可见 focus 状态。

## 进度更新

监督 Agent 和子 agents 必须持续维护任务状态：

- 子 agent 完成 checklist 项时，立即更新对应 `doc/tasks/<module-name>.md`。
- 模块完成后，监督 Agent 更新 `doc/tasks/progress.md` 的模块进度。
- 发现失败时，监督 Agent 在 `progress.md` 记录失败命令、失败摘要、负责修复的子 agent 和重试结果。
- 发现阻塞时，在对应任务文件和 `progress.md` 写明阻塞原因、已尝试方案、影响范围和下一步自动处理方案。
- 最终所有可完成项必须标记为完成，阻塞项必须有明确证据。

## 最终交付

最终回复必须直接说明：

1. 完成了哪些模块。
2. 修改了哪些关键文件。
3. 补充了哪些 pytest 单元测试。
4. 运行了哪些验证命令及结果。
5. 手动 smoke test 结果。
6. 仍然存在的风险或未完成项。
7. 本地运行方式。

不要输出与本项目无关的建议。不要要求人工参与实现过程。
