# 数据模型模块

## 模块目标

定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- `src/app.js`

## 不做什么

- 不直接操作 DOM。
- 不直接读写 `localStorage`。
- 不实现筛选、指标计算或 JSON 导入导出。

## 任务 checklist

- [x] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
- [x] 定义状态集合：`backlog`、`doing`、`review`、`done`。
- [x] 定义优先级集合：`low`、`medium`、`high`。
- [x] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
- [x] 定义优先级显示文案映射，用于卡片和表单展示。
- [x] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
- [x] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
- [x] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
- [x] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
- [x] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。

## 验收标准

- 数据结构与设计文档中的任务对象一致。
- 状态、优先级和筛选默认值可被后续模块复用。
- 存储 key 固定且只定义一处。
- 模块加载时不会因为缺少浏览器 API 报错。

## 测试要求

- [x] 使用契约测试确认固定存储 key 仍符合要求。
- [x] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。

## 验证记录

- `python3 -m unittest discover -s tests` 通过，确认固定 key、named functions 和 DOM 启动保护契约。
- Node-backed 逻辑断言直接导入 `src/app.js` 通过，确认非浏览器环境不会访问 DOM。

## 风险和注意事项

- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
- 显示文案可以变化，但内部值不可随意变化。
