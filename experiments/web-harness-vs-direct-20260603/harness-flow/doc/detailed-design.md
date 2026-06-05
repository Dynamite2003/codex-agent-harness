# Sprint Board Lite 详细设计文档

## 目标

将 `doc/proposal.md` 中的需求转化为可实现的静态 Web 应用设计，明确 Sprint Board Lite 的页面结构、状态模型、模块划分、模块关系、数据归一化、持久化、渲染流程、筛选逻辑、JSON 导入导出交互，以及响应式和可访问性要求。

本设计只覆盖 HTML、CSS、JavaScript 的实现方案，不生成任务清单，不修改业务代码，不引入后端、构建工具、框架、远程资源或第三方依赖。

## 输入

- 需求文档：`doc/proposal.md`
- 设计阶段补充决策：
  - JSON 导入采用替换当前任务列表，不做合并。
  - JSON 导入同时接受任务数组，以及包含 `tasks` 数组的对象；其他格式报错且不覆盖现有数据。
  - 删除任务不需要二次确认。
  - 负责人筛选只从当前任务负责人自动生成选项，包含 `All`。
  - 完成百分比按 `done` 状态的任务数量 / 总任务数量计算，不按工作量加权。

## 输出

本文档作为设计阶段输出：`doc/detailed-design.md`。

后续实现阶段应基于本文档修改 `index.html`、`src/styles.css`、`src/app.js`，并保持现有契约测试要求的文件结构、元素、函数名、样式 selector、存储 key 和基本文案约束。

## 步骤

1. 从需求文档抽取功能边界、技术约束、测试约束和用户场景。
2. 将应用拆分为数据模型、归一化、持久化、指标计算、筛选、渲染、交互控制、导入导出、样式与可访问性模块。
3. 定义模块之间的数据流和调用关系，保证所有任务变更都经过归一化、状态更新、持久化和重新渲染。
4. 固化设计阶段已确认的产品规则，包括导入替换、导入格式、删除行为、负责人筛选来源和完成百分比算法。
5. 描述边界情况和验证关注点，供后续实现阶段对照。

## 总体架构

Sprint Board Lite 是一个 dependency-free 的浏览器端静态应用，由三类文件组成：

| 文件 | 设计职责 |
| --- | --- |
| `index.html` | 提供语义化页面骨架、表单、筛选器、KPI 容器、看板列、导入导出控件和可访问 label。 |
| `src/styles.css` | 提供紧凑 dashboard 布局、响应式网格、任务卡片、状态标识、表单控件、focus 状态和移动端适配。 |
| `src/app.js` | 管理任务状态、数据归一化、localStorage 持久化、指标计算、筛选、DOM 渲染、事件绑定和 JSON 导入导出。 |

应用不依赖后端。所有任务数据保存在浏览器 `localStorage` 中，固定 key 为 `sprint-board-lite.tasks.v1`。首屏直接呈现可工作的看板、任务表单、筛选器和指标，不提供营销页。

## 模块划分

### 1. 页面结构模块

页面应采用工作工具式布局：

- 顶部 header 显示产品名 `Sprint Board Lite`。
- 主区域包含 KPI 指标区、任务录入表单、筛选与导入导出工具区、四列看板。
- 四个看板列固定为 `backlog`、`doing`、`review`、`done`，每列使用 `data-status` 标识状态。
- 表单字段覆盖标题、负责人、工作量、优先级、状态和备注。
- 搜索、状态筛选、负责人筛选与导入导出控件位于看板附近，便于高频操作。

页面结构应保留契约测试要求的必要元素 id、文本和 selector。设计上不依赖动态创建整个页面骨架，静态 HTML 应提供主要容器，JavaScript 负责填充指标、筛选选项和任务卡片。

### 2. 数据模型模块

任务对象采用统一内部结构：

```js
{
  id: "stable-string-id",
  title: "Task title",
  owner: "Owner name",
  effort: 0,
  priority: "low" | "medium" | "high",
  status: "backlog" | "doing" | "review" | "done",
  notes: "Free text notes"
}
```

字段规则：

- `id` 用于事件定位和删除、状态更新。缺失时生成稳定字符串 id。
- `title` 需要 trim。表单新增时，空标题或纯空白标题不创建任务。
- `owner` 需要 trim。空负责人可归一化为简洁默认值，例如 `Unassigned`。
- `effort` 归一化为有限、非负数字。无效、负数、`NaN` 或无限值归一化为 `0`。
- `priority` 只允许 `low`、`medium`、`high`，无效值归一化为 `medium`。
- `status` 只允许 `backlog`、`doing`、`review`、`done`，无效值归一化为 `backlog`。
- `notes` 归一化为字符串，缺失时为空字符串。

导入或读取存储数据时，空标题记录不应进入看板，避免产生不可识别任务卡片。

### 3. 数据归一化模块

`normalizeTask` 是所有外部输入进入内部状态前的入口，包括表单提交、localStorage 读取、sample tasks 初始化和 JSON 导入。

设计约束：

- 函数接收任意对象并返回标准任务对象，或由调用方过滤掉无有效标题的输入。
- 函数不直接读写 DOM。
- 函数不直接读写 `localStorage`。
- 函数应可在非浏览器环境中被测试调用。

归一化顺序：

1. 读取并 trim `title`、`owner`、`notes`。
2. 解析并限制 `effort` 为有限、非负数字。
3. 校验 `priority` 和 `status` 是否在允许集合内。
4. 保留已有 `id`，缺失时生成新 id。
5. 返回内部任务对象。

### 4. 持久化模块

持久化模块由 `saveTasks` 和 `loadTasks` 负责。

`saveTasks(tasks)`：

- 对传入任务列表执行可序列化处理。
- 使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
- 在 `localStorage` 不可用时不使应用崩溃，可降级为 no-op 或返回失败状态。

`loadTasks()`：

- 当 `localStorage` 中没有固定 key 时，加载少量 sample tasks，并可保存为初始数据。
- 当固定 key 存在时，解析 JSON 并归一化任务列表。
- 当存储 JSON 损坏或格式不符合任务列表时，返回空任务列表或可恢复结果，不因为异常阻塞页面渲染。
- 不在非浏览器环境中直接假设 `window` 或 `localStorage` 一定存在。

sample tasks 只在固定 key 缺失时使用。固定 key 已存在但内容为空数组、损坏或无有效任务时，不应再次 seed sample tasks。

### 5. 指标计算模块

`calculateMetrics(tasks)` 基于完整当前任务列表计算指标，不受搜索或筛选条件影响。

输出指标包括：

| 指标 | 计算方式 |
| --- | --- |
| 总任务数 | `tasks.length` |
| 完成百分比 | `done` 状态任务数 / 总任务数；总数为 `0` 时显示 `0%` |
| 总工作量 | 所有任务 `effort` 求和 |
| 未完成高优先级任务数 | `priority === "high"` 且 `status !== "done"` 的任务数量 |

完成百分比不按工作量加权。显示值建议四舍五入到整数百分比，保持 dashboard 易读。

### 6. 筛选模块

`filterTasks(tasks, filters)` 接收完整任务列表和筛选条件，返回可见任务列表。

筛选条件：

- `query`：关键词搜索，大小写不敏感。匹配范围至少包括标题、负责人和备注。
- `status`：`All` 或四个状态之一。
- `owner`：`All` 或当前任务负责人之一。

负责人筛选选项由当前完整任务列表自动生成：

- 第一个选项固定为 `All`。
- 其余选项来自当前任务的负责人字段，去重后显示。
- 新增、删除、导入任务后需要重新生成负责人选项。
- 搜索和状态筛选只影响可见任务，不改变负责人选项来源。

筛选结果为空时，看板仍显示四列。每个没有可见任务的列显示简洁 empty state。

### 7. 看板渲染模块

`renderBoard(tasks, filters)` 负责将状态渲染到 DOM。

渲染输入：

- 完整任务列表。
- 当前筛选条件。
- 固定状态列定义。

渲染输出：

- KPI 指标文本。
- 负责人筛选选项。
- 每列任务卡片。
- 每列 empty state。
- 导入失败或成功反馈。

渲染流程：

1. 使用 `calculateMetrics` 计算完整任务列表指标。
2. 使用 `filterTasks` 得到可见任务。
3. 按 `status` 将可见任务分组到四列。
4. 清空每列任务容器。
5. 为每个可见任务创建卡片 DOM。
6. 对空列插入 empty state。
7. 更新 KPI 和辅助反馈区域。

任务卡片显示标题、负责人、工作量、优先级、状态和备注。卡片上提供状态变更控件和删除控件。状态变更后更新任务对象、保存任务、重新渲染。删除任务不进行二次确认，直接从当前任务列表移除、保存并重新渲染。

### 8. 交互控制模块

DOM 启动逻辑应被保护：

```js
if (typeof document !== "undefined") {
  // bind events and render
}
```

启动流程：

1. 等待 DOM 可用。
2. 通过 `loadTasks()` 初始化 `appState.tasks`。
3. 初始化 `appState.filters` 为搜索空、状态 `All`、负责人 `All`。
4. 绑定表单、筛选、状态变更、删除、导出、导入事件。
5. 调用 `renderBoard()` 完成首屏渲染。

状态管理采用单一内存状态对象：

```js
{
  tasks: [],
  filters: {
    query: "",
    status: "All",
    owner: "All"
  }
}
```

交互规则：

- 表单提交：读取字段，标题无效则给出简洁反馈且不新增；有效则归一化、追加、保存、重渲染并清理表单。
- 搜索输入：更新 `filters.query` 并重渲染，不写入 localStorage。
- 状态筛选：更新 `filters.status` 并重渲染。
- 负责人筛选：更新 `filters.owner` 并重渲染。
- 卡片状态变更：按 `id` 查找任务，更新状态，保存，重渲染。
- 删除任务：按 `id` 删除，保存，重渲染，不弹二次确认。

推荐使用事件委托处理卡片内的状态变更和删除，减少每次渲染后的重复绑定。

### 9. JSON 导出导入模块

导出：

- 导出当前完整任务列表，而不是当前筛选后的可见任务。
- 输出 JSON 建议为任务数组，使用 `JSON.stringify(tasks, null, 2)` 提升可读性。
- 通过 Blob 和临时下载链接生成本地 JSON 文件。
- 导出不改变当前任务状态。

导入：

- 接受两种合法格式：
  - 任务数组：`[{...}, {...}]`
  - 包含 `tasks` 数组的对象：`{"tasks": [{...}, {...}]}`
- 其他格式视为错误。
- 格式错误、JSON 解析失败或 `tasks` 不是数组时，显示简洁错误反馈，不覆盖现有任务数据。
- 合法导入会对每个任务执行归一化，并用结果替换当前完整任务列表，不做合并。
- 成功导入后立即保存到 `localStorage`，重新生成负责人筛选选项，并重新渲染看板。

导入替换规则必须是原子性的：只有在解析、格式识别和归一化流程完成后，才更新 `appState.tasks` 和持久化数据。

### 10. 样式和响应式模块

视觉风格应是安静、密集、实用的 dashboard 工具界面。

布局设计：

- 桌面端使用 header、KPI 横向网格、表单和筛选工具区、四列看板网格。
- 看板列应有稳定宽度和最小高度，避免内容变化导致布局跳动。
- 卡片使用清晰边界、紧凑间距和状态标识。
- 移动端将 KPI、表单、筛选器和看板列纵向堆叠，保证文本不重叠。

样式约束：

- 不使用外部字体、图片、远程 CDN 或装饰性渐变。
- 不使用过度装饰的 landing page 视觉。
- 所有按钮、输入框、select 和文件输入需要可见 focus 状态。
- 文本尺寸不依赖 viewport width 缩放。
- 颜色系统应以中性色为主体，使用有限的状态色区分优先级和任务状态。

### 11. 可访问性模块

可访问性要求：

- 所有表单控件使用显式 `label`，并通过 `for` 关联控件 id。
- 交互按钮使用清晰文本，例如新增、删除、导出、导入。
- 状态变更控件具备可理解的 label 或上下文。
- 反馈区域可使用 `aria-live="polite"`，用于导入失败、导入成功和表单校验提示。
- 任务卡片中的信息不只依赖颜色表达，优先级和状态需要文本展示。
- 键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。

## 模块关系

核心数据流：

```text
loadTasks
  -> normalizeTask
  -> appState.tasks
  -> renderBoard
  -> calculateMetrics
  -> filterTasks
  -> DOM
```

新增任务数据流：

```text
form submit
  -> read form values
  -> normalizeTask
  -> append to appState.tasks
  -> saveTasks
  -> renderBoard
```

筛选数据流：

```text
search/status/owner change
  -> update appState.filters
  -> renderBoard
  -> filterTasks
  -> DOM
```

状态更新数据流：

```text
card status control change
  -> find task by id
  -> update status
  -> saveTasks
  -> renderBoard
```

删除数据流：

```text
delete control click
  -> remove task by id
  -> saveTasks
  -> renderBoard
```

导入数据流：

```text
file input/change or import action
  -> read file text
  -> JSON.parse
  -> accept array or object.tasks array
  -> normalize imported tasks
  -> replace appState.tasks
  -> saveTasks
  -> renderBoard
```

导出数据流：

```text
export action
  -> JSON.stringify appState.tasks
  -> Blob
  -> download JSON
```

## JavaScript 公共函数设计

`src/app.js` 必须暴露以下 named functions：

- `normalizeTask`
- `calculateMetrics`
- `filterTasks`
- `saveTasks`
- `loadTasks`
- `renderBoard`

这些函数需要具备以下特征：

- 可被契约测试直接发现或调用。
- 不在模块加载时依赖 DOM 已存在。
- 不在模块加载时立即访问不可用的浏览器 API。
- 纯计算函数尽量保持无副作用，特别是 `normalizeTask`、`calculateMetrics`、`filterTasks`。
- 浏览器环境中可将函数挂载到 `window`，便于调试和测试；非浏览器环境不应因此报错。

## 边界情况

- 空任务列表：KPI 显示总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`，四列显示 empty state。
- 全部任务完成：完成百分比显示 `100%`，未完成高优先级任务数为 `0`。
- 筛选无结果：KPI 仍显示完整任务列表指标，看板列显示 empty state。
- owner 被删除后：负责人选项重新生成；如果当前筛选 owner 已不存在，应回退到 `All`。
- localStorage 缺失：使用 sample tasks 初始化。
- localStorage 损坏：不阻塞页面渲染，不再次 seed sample tasks。
- 导入空数组：视为合法导入，替换为无任务状态。
- 导入非法 JSON：显示错误，不覆盖现有任务。
- 导入合法对象但无 `tasks` 数组：显示错误，不覆盖现有任务。
- 工作量输入为空、负数、非数字或无限值：归一化为 `0`。

## 验证关注点

后续实现完成后，应验证以下行为符合设计：

- 页面打开后首屏是可操作看板。
- 固定存储 key 为 `sprint-board-lite.tasks.v1`。
- 六个 named functions 存在，并且 DOM 启动逻辑有环境保护。
- 新增、删除、状态变更和导入后，KPI、看板和 localStorage 同步更新。
- JSON 导入替换当前任务列表，不合并。
- JSON 导入只接受数组或包含 `tasks` 数组的对象。
- 负责人筛选来自当前任务负责人，并包含 `All`。
- 完成百分比按 done 任务数量计算。
- 移动端布局不出现文字重叠，所有表单控件有可访问 label。
