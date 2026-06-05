# Sprint Board Lite 总体任务进度

## 目标

基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。

## 模块进度

- [x] 页面结构模块：`doc/tasks/page-structure.md`
- [x] 数据模型模块：`doc/tasks/data-model.md`
- [x] 数据归一化模块：`doc/tasks/normalization.md`
- [x] 持久化模块：`doc/tasks/persistence.md`
- [x] 指标计算模块：`doc/tasks/metrics.md`
- [x] 筛选模块：`doc/tasks/filtering.md`
- [x] 看板渲染模块：`doc/tasks/board-rendering.md`
- [x] 交互控制模块：`doc/tasks/interactions.md`
- [x] JSON 导入导出模块：`doc/tasks/json-import-export.md`
- [x] 样式和响应式模块：`doc/tasks/styles-responsive.md`
- [x] 可访问性模块：`doc/tasks/accessibility.md`
- [x] 验证模块：`doc/tasks/verification.md`

## 推荐执行顺序

1. 页面结构模块
2. 数据模型模块
3. 数据归一化模块
4. 持久化模块
5. 指标计算模块
6. 筛选模块
7. 看板渲染模块
8. 交互控制模块
9. JSON 导入导出模块
10. 样式和响应式模块
11. 可访问性模块
12. 验证模块

## 可并行项

- [x] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
- [x] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
- [x] 可访问性可以与页面结构、交互控制和样式模块同步检查。
- [x] JSON 导出导入可以在持久化和归一化模块完成后独立实现。

## 阻塞项

- [x] 当前无实现阻塞；契约测试与设计文档未发现硬冲突。
- [x] 验证环境阻塞：`uv` 不在 PATH；当前 Python 环境缺少 `pytest`、`mypy`、`ruff`；真实浏览器 smoke 受限于端口绑定被沙箱拒绝、in-app Browser 不可用、Playwright 包不可用。已执行 Python 语法编译、unittest、focused pytest-style 直接调用、Node-backed 逻辑断言和内存 DOM smoke 作为可用验证。

## 跨模块注意事项

- [x] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
- [x] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
- [x] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
- [x] JSON 导入必须原子替换完整任务列表，不做合并。
- [x] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
- [x] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
- [x] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。

## 实现阶段记录

- 页面结构子 agent 完成 `index.html` 与 `doc/tasks/page-structure.md`；样式子 agent 完成初版 `src/styles.css` 与 `doc/tasks/styles-responsive.md`。监督 Agent 对 `src/app.js`、focused tests、样式收敛和任务记录进行了合并与复核。
- 新增 `tests/test_app_logic.py` 和 `pyproject.toml`，不修改、不删除、不跳过、不弱化 `tests/test_static_contract.py`。
- `python3 -m unittest discover -s tests`：通过，6 tests OK。
- `python3 -m py_compile tests/test_app_logic.py tests/test_static_contract.py`：通过。
- focused pytest-style 测试函数直接调用：通过。
- Node-backed `src/app.js` 逻辑断言：通过。
- 内存 DOM smoke：通过，覆盖新增、空标题、状态移动、删除、搜索/筛选、empty state、导出、数组导入、对象导入、非法导入不覆盖、刷新恢复。
- CSS 禁止项扫描：未发现外部 URL/CDN、Google Fonts、渐变或 viewport 字体缩放写法。
