# 持久化模块

## 模块目标

实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- 数据模型模块输出
- 数据归一化模块输出
- `src/app.js`

## 不做什么

- 不渲染 DOM。
- 不处理筛选条件。
- 不实现 JSON 文件导入导出。

## 任务 checklist

- [x] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
- [x] 在保存前确保写入的是可序列化任务数组。
- [x] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
- [x] 实现 `loadTasks()` named function，并保护非浏览器环境。
- [x] 当固定 key 不存在时，加载少量有用 sample tasks。
- [x] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
- [x] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
- [x] 对读取到的每条任务执行 `normalizeTask`。
- [x] 过滤空标题任务，避免无效任务进入应用状态。
- [x] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。

## 验收标准

- 首次打开且无固定 key 时出现 sample tasks。
- 固定 key 存在为空数组时，看板保持空任务状态。
- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
- 保存、新增、删除、状态变更和导入后使用同一个固定 key。

## 测试要求

- [x] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
- [x] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
- [x] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。

## 验证记录

- `tests/test_app_logic.py` 覆盖 key 缺失、空数组、损坏 JSON、无效任务过滤、保存归一化。
- Node-backed localStorage mock 断言通过：key 缺失 seed sample tasks；key 存在为空数组、损坏或仅无效任务时不重新 seed。

## 风险和注意事项

- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
