# 数据归一化模块

## 模块目标

实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- 数据模型模块输出
- `src/app.js`

## 不做什么

- 不读写 DOM。
- 不读写 `localStorage`。
- 不决定任务是否保存或渲染。

## 任务 checklist

- [x] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
- [x] 将 `title` 转为字符串并 trim。
- [x] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
- [x] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
- [x] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
- [x] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
- [x] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
- [x] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
- [x] 在调用方过滤空标题任务，保证空标题记录不进入看板。
- [x] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。

## 验收标准

- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
- 归一化函数不产生 DOM 或存储副作用。
- 空标题任务不会被新增、导入或从存储中恢复到看板。
- 无效状态、优先级和工作量不会破坏界面。

## 测试要求

- [x] 补充或运行测试覆盖有效任务归一化。
- [x] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
- [x] 验证缺失 id 时生成字符串 id，已有 id 时保留。

## 验证记录

- `tests/test_app_logic.py` 覆盖有效输入、空标题、空负责人、无效工作量、非法优先级、非法状态、id 保留和 id 生成。
- 当前环境缺少 `pytest` 包；已用 Python 标准库直接调用新增 pytest-style 测试函数，全部通过。
- Node-backed 逻辑断言直接执行 `normalizeTask`，全部通过。

## 风险和注意事项

- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
