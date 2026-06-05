# 看板渲染模块

## 模块目标

实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- 页面结构模块输出
- 指标计算模块输出
- 筛选模块输出
- `src/app.js`

## 不做什么

- 不绑定全局启动事件。
- 不直接读取表单输入。
- 不直接解析 JSON 文件。

## 任务 checklist

- [x] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
- [x] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
- [x] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
- [x] 使用 `filterTasks` 计算可见任务。
- [x] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
- [x] 每次渲染前清空四列任务容器，避免重复卡片。
- [x] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
- [x] 为每个任务卡片创建状态变更控件。
- [x] 为每个任务卡片创建删除控件，并携带可定位任务 id。
- [x] 为没有可见任务的列插入简洁 empty state。
- [x] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
- [x] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。

## 验收标准

- 所有任务变更后重渲染不会产生重复卡片。
- KPI 始终显示完整任务列表指标。
- 空列显示 empty state。
- 卡片包含需求文档列出的所有任务字段。
- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。

## 测试要求

- [x] 运行契约测试，确认 `renderBoard` 存在。
- [x] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
- [x] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。

## 验证记录

- `python3 -m unittest discover -s tests` 通过，确认 `renderBoard` named function 存在。
- 内存 DOM smoke 覆盖首屏四列 sample tasks、筛选无结果四列 empty state、新增、状态变更、删除、数组导入、对象导入后的重渲染。

## 风险和注意事项

- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
- 重建 owner 选项时不要错误清空用户当前有效筛选值。
