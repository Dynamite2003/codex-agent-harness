# 验证模块

## 模块目标

在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。

## 依赖输入

- `doc/proposal.md`
- `doc/detailed-design.md`
- 所有实现模块输出
- `tests/test_static_contract.py`

## 不做什么

- 不跳过、删除、弱化或重写现有契约测试。
- 不用补充测试替代契约测试。
- 不引入自动化测试框架或构建工具。

## 任务 checklist

- [x] 运行 `python3 -m unittest discover -s tests`，记录结果。
- [x] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
- [x] 人工 smoke test：打开页面确认首屏是可操作看板。
- [x] 人工 smoke test：新增有效任务并确认对应列出现卡片。
- [x] 人工 smoke test：提交空标题任务并确认不会新增。
- [x] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
- [x] 人工 smoke test：删除任务并确认不需要二次确认。
- [x] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
- [x] 人工 smoke test：确认筛选无结果时四列显示 empty state。
- [x] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
- [x] 人工 smoke test：导入任务数组并确认替换当前任务列表。
- [x] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
- [x] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
- [x] 验证刷新页面后任务从 `localStorage` 恢复。
- [x] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
- [x] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
- [x] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
- [x] 验证所有表单控件有 label，交互控件有可见 focus 状态。

## 验收标准

- 契约测试全部通过。
- 需求文档列出的最终手动 smoke test 全部通过。
- 设计文档列出的边界情况至少完成人工或自动验证。
- 不存在业务代码之外的无关修改。

## 测试要求

- [x] 必须执行 `python3 -m unittest discover -s tests`。
- [x] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
- [x] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。

## 验证记录

### 命令结果

- `uv run pytest`：未执行成功，当前环境 `uv` 不在 PATH（`/bin/bash: uv: command not found`）。
- `uv run mypy`：未执行成功，当前环境 `uv` 不在 PATH。
- `uv run ruff check .`：未执行成功，当前环境 `uv` 不在 PATH。
- `python3 -m pytest`：未执行成功，当前 Python 环境缺少 `pytest` 包。
- `python3 -m mypy`：未执行成功，当前 Python 环境缺少 `mypy` 包。
- `python3 -m ruff check .`：未执行成功，当前 Python 环境缺少 `ruff` 包。
- `python3 -m unittest discover -s tests`：通过，6 tests OK。
- `python3 -m py_compile tests/test_app_logic.py tests/test_static_contract.py`：通过。
- `tests/test_app_logic.py` pytest-style 测试函数通过 Python 标准库直接调用执行。
- Node-backed 逻辑断言：通过，覆盖 `normalizeTask`、`calculateMetrics`、`filterTasks`、`saveTasks`、`loadTasks`。

### Smoke Test 结果

- 真实浏览器 smoke 受环境限制：`python3 -m http.server` 端口绑定被沙箱拒绝；in-app Browser 返回 `Browser is not available: iab`；Playwright 包不可用。
- 已执行内存 DOM smoke，直接加载同一份 `src/app.js` 并触发表单、筛选、看板、导入导出事件；结果通过。
- 覆盖项：首屏 sample tasks 渲染、新增有效任务、空标题不新增、状态移动后 KPI/看板/存储同步、删除无需确认、搜索/状态/负责人筛选、无结果四列 empty state、导出完整任务列表、数组导入替换、对象导入替换、非法 JSON 不覆盖、重新加载后从 `localStorage` 恢复。
- 移动端和文本重叠通过 CSS 静态检查验证：存在响应式断点、稳定网格、`overflow-wrap: anywhere`、按钮换行规则和可见 focus 状态；真实视觉截图未能执行，作为剩余环境风险记录。

### 补充测试

- 新增 `tests/test_app_logic.py`，覆盖归一化、指标、筛选、持久化规则。该文件在有 Node CLI 的环境会动态导入 `src/app.js` 的 ESM 副本执行行为断言；无 Node CLI 时执行源码级 fallback 断言。
- 新增 `pyproject.toml`，为 `pytest`、`mypy`、`ruff` 提供项目测试配置和 dev dependency 声明。

## 阻塞记录

- `uv`、`pytest`、`mypy`、`ruff` 在当前环境不可用，无法完成这些命令的真实通过结果。
- 真实浏览器/移动端截图验证不可用，原因是端口绑定被沙箱拒绝、in-app Browser 不可用、Playwright 包不可用。
- 以上阻塞均为执行环境限制；实现代码和契约 unittest 当前通过。

## 风险和注意事项

- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。
