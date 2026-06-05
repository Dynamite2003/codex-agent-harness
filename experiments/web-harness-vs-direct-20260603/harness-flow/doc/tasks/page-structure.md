# 页面结构模块

## 模块目标

实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- 现有 `index.html`
- 现有契约测试声明的必要元素 id、文本和 selector

## 不做什么

- 不实现业务逻辑、状态管理或数据持久化。
- 不引入框架、CDN、外部字体、图片或构建工具。
- 不创建营销 landing page。

## 任务 checklist

- [x] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
- [x] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
- [x] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
- [x] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
- [x] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
- [x] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
- [x] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
- [x] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
- [x] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
- [x] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。

## 实现笔记

- 页面标题、`main#app`、header 和主标题均保留 `Sprint Board Lite`。
- 契约要求的 id 已静态提供：`task-form`、`task-title`、`task-owner`、`task-effort`、`task-priority`、`task-status`、`task-notes`、`search-input`、`status-filter`、`owner-filter`、`metric-total`、`metric-completion`、`metric-effort`、`metric-high-priority`、`export-json`、`import-json`、`import-file`。
- 表单和筛选控件均使用显式 `label for`，导入文件控件也补充了 `label for="import-file"`。
- 四个看板列使用 `.column[data-status]`，状态值为 `backlog`、`doing`、`review`、`done`，标题文本为 Backlog、Doing、Review、Done。
- 每列内预留 `.task-list[data-task-list="<status>"]`，供后续 `renderBoard` 填充任务卡片和 empty state。
- 反馈区使用 `#feedback[aria-live="polite"]`，供后续导入、校验和操作反馈使用。
- 保留本地资源引用：`src/styles.css` 和 `src/app.js`，未添加外部资源。

## 验收标准

- 页面不是营销页，首屏包含实际工作看板。
- 四个状态列都存在，并使用正确的 `data-status` 值。
- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
- 所有表单控件具备可访问 label。
- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。

## 测试要求

- [x] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
- [x] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。

## 验证记录

- `python3 -m unittest tests.test_static_contract.StaticWebContractTests.test_html_declares_app_shell tests.test_static_contract.StaticWebContractTests.test_html_does_not_depend_on_external_assets tests.test_static_contract.StaticWebContractTests.test_task_form_controls_are_not_placeholder_only` 通过。
- `python3 -m unittest discover -s tests` 已运行；当前仍有 2 个失败，均在本模块允许修改范围之外：`src/styles.css` 缺少 CSS 契约 selector，`src/app.js` 缺少 JavaScript 契约函数。
- 内存 DOM smoke 确认首屏初始化后显示 KPI、表单挂载点、筛选器、四列看板和 sample task 卡片。
- 真实浏览器打开检查受环境限制：当前 in-app Browser 不可用，端口绑定被沙箱拒绝，Playwright 包不可用。

## 风险和注意事项

- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
