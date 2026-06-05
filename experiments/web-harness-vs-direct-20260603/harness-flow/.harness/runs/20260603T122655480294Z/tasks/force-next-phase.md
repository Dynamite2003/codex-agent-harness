当前阶段收到 Codex 继续反问，但用户选择强制进入下一阶段。

### Ignored Codex Questions

已完成任务阶段产物，未修改业务代码。

生成内容：
- 总体进度：[progress.md](/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md)
- 模块任务文件：`page-structure`、`data-model`、`normalization`、`persistence`、`metrics`、`filtering`、`board-rendering`、`interactions`、`json-import-export`、`styles-responsive`、`accessibility`
- 额外验证模块：`verification.md`，用于承接契约测试和手动 smoke test 约束

我已核对 `doc/tasks` 下共 13 个 Markdown 文件，均使用 checklist 表示任务状态。没有发现会阻塞任务划分的未明确点，因此未向你追加提问。

OpenAI Codex v0.135.0
--------
workdir: /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
model: gpt-5.5
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: xhigh
reasoning summaries: none
session id: 019e8d80-819f-7432-8951-dd9a153c2a68
--------
user
目标：
为每一个模块划分最小可执行的任务。

输入：
需求文档：doc/proposal.md；设计文档：doc/detailed-design.md。
当前解析到的输入文档：
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/proposal.md (exists)
- /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/detailed-design.md (exists)
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 任务 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
任务列表：
- doc/tasks/<module-name>.md（每一个模块对应一个）。
- doc/tasks/progress.md（总体进度）。

步骤：
根据需求文档和详细设计，为每一个模块生成 vibe coding 的最小任务。
每一个模块对应一个 <module-name>.md，用 checklist 表示子任务是否完成。
在 progress.md 中用 checklist 表示模块是否完成。
任何会影响任务划分的不明确点必须向用户询问，不要猜测我的意图。
不要修改业务代码。

codex
我会使用 `expand-tasks-prompt` 技能来按现有需求和设计文档生成任务拆分；先读取技能要求和两份输入文档，再写入 `doc/tasks`。
exec
/bin/bash -lc "sed -n '1,220p' /Users/bytedance/.codex/skills/expand-tasks-prompt/SKILL.md" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
---
name: expand-tasks-prompt
description: Expand requirements and design artifacts into a complete Chinese task-breakdown prompt for Codex. Use when the user says 任务 prompt, 任务拆分, task breakdown, progress.md, or wants Codex to create doc/tasks/progress.md and per-module task checklists from doc/proposal.md and doc/detailed-design.md without running a full harness.
---

# Expand Tasks Prompt

## Workflow

Take the user's planning artifacts or short description and return one copy-ready prompt in Chinese for generating implementation task files. Do not implement code.

Default inputs are `doc/proposal.md` and `doc/detailed-design.md`. Default outputs are `doc/tasks/progress.md` and `doc/tasks/<module-name>.md`.

## Output Shape

Return only the expanded prompt, preferably in a fenced `text` block. Include these sections:

- 目标
- 输入
- 输出
- 步骤
- 任务粒度规则
- 质量要求

## Tasks Prompt Template

```text
你是一个资深技术负责人。现在只完成任务拆分阶段，不写业务代码。

目标：
基于需求文档和详细设计，将项目拆成最小可执行、可验证、适合逐步实现的任务清单。

输入：
- 需求文档：[默认 doc/proposal.md]
- 详细设计文档：[默认 doc/detailed-design.md]
- 当前项目目录：[如已知则填写；未知则读取当前工作区]

输出：
请生成或更新：
- doc/tasks/progress.md：总体模块进度 checklist
- doc/tasks/<module-name>.md：每个模块一个任务文件

每个模块任务文件必须包含：
1. 模块目标
2. 依赖输入
3. 不做什么
4. 任务 checklist
5. 验收标准
6. 测试要求
7. 风险和注意事项

步骤：
1. 阅读需求和设计文档，识别模块边界、依赖关系和可并行工作。
2. 为每个模块创建一个清晰的任务文件，文件名使用英文小写短横线。
3. 将任务拆到 0.5-2 小时内可完成的粒度；每个任务必须有明确产出。
4. 在 progress.md 中列出模块总览、推荐执行顺序、可并行项和阻塞项。
5. 对跨模块依赖、数据库迁移、外部服务、环境变量、测试数据和验收方式单独列明。
6. 如发现需求或设计存在阻塞矛盾，先向用户提问；否则记录为待确认并继续拆分。
7. 不要修改业务代码，不要安装依赖，不要启动服务。

任务粒度规则：
- 每个 checklist 项必须以动词开头，例如“实现...”“补充...”“验证...”。
- 每个任务必须能被测试或人工验收。
- 不要写“优化体验”“完善功能”这类不可验收任务，除非拆成具体行为。
- 优先把基础设施、数据模型、核心流程、测试、错误状态和文档分开。

质量要求：
- 任务清单要能直接交给实现 agent 执行。
- 覆盖前端、后端、数据、外部集成、权限、安全、测试和发布验证。
- 保持 MVP 范围，不引入设计文档未要求的大功能。
```

exec
/bin/bash -lc 'find doc -maxdepth 3 -type f | sort' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
exec
/bin/bash -lc "sed -n '1,320p' doc/detailed-design.md" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
exec
/bin/bash -lc "sed -n '1,260p' doc/proposal.md" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
doc/detailed-design.md
doc/proposal.md

 succeeded in 0ms:
# Sprint Board Lite 需求文档

## 背景

Sprint Board Lite 是一个面向小团队的轻量级冲刺看板。项目当前已有最小静态 Web scaffold 和 Python unittest 契约测试，用于约束最终交付的 HTML、CSS、JavaScript 文件结构与关键行为。

应用需要直接在浏览器中运行，不依赖后端服务。首屏必须是可工作的冲刺看板，而不是营销页或介绍页。

## 目标

- 构建一个 dependency-free 的静态 Web 应用：Sprint Board Lite。
- 帮助小团队在浏览器中规划、查看、筛选、更新和删除冲刺任务。
- 在无后端的前提下通过 `localStorage` 持久化任务数据。
- 提供 JSON 导出和导入能力，便于备份或迁移任务数据。
- 满足现有契约测试，并保留测试对结构、函数、样式和基本行为的约束。

## 输入

- 当前项目目录：`/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow`
- 现有 scaffold：
  - `index.html`
  - `src/styles.css`
  - `src/app.js`
  - `tests/test_static_contract.py`
- 用户给定的产品与技术需求。
- 现有契约测试中声明的必须存在的元素 id、函数名、样式 selector、存储 key 和基本文本。

## 输出

需求阶段输出为本文档：`doc/proposal.md`。

后续阶段应基于本文档进入设计，不应依赖需求阶段聊天历史。

## 非目标

- 不实现后端、数据库、用户登录、多用户协作或服务端同步。
- 不引入 npm、构建工具、框架、远程 CDN、外部字体或第三方资源。
- 不构建营销 landing page。
- 不实现复杂项目管理能力，例如泳道、甘特图、依赖关系、自动排期、权限、评论线程或通知。
- 不删除、跳过、弱化或重写现有契约测试。
- 当前阶段不做设计、任务拆分或代码实现。

## 用户故事或使用场景

- 作为团队成员，我希望打开页面后直接看到冲刺看板，以便快速了解当前工作状态。
- 作为团队成员，我希望新增任务并填写标题、负责人、工作量、优先级、状态和备注，以便记录冲刺事项。
- 作为团队成员，我希望看到总任务数、完成百分比、总工作量和未完成高优先级任务数，以便快速判断冲刺健康度。
- 作为团队成员，我希望按关键词、状态和负责人筛选任务，以便在任务较多时快速定位。
- 作为团队成员，我希望在卡片上直接调整任务状态，以便把任务从 Backlog 推进到 Doing、Review 或 Done。
- 作为团队成员，我希望删除不再需要的任务，以便保持看板干净。
- 作为团队成员，我希望导出任务 JSON，以便备份当前看板。
- 作为团队成员，我希望导入任务 JSON，以便恢复或迁移看板数据。
- 作为移动端用户，我希望窄屏下页面仍然可读、可操作，不出现文字重叠。

## 功能需求

### 页面结构

- 页面标题和主标题应包含产品名 `Sprint Board Lite`。
- 页面应包含 concise header，用于显示产品名称。
- 首屏应展示实际工作看板和任务操作区域。
- 应实现以下文件：
  - `index.html`
  - `src/styles.css`
  - `src/app.js`

### KPI 指标

- 显示总任务数。
- 显示完成百分比。
- 显示总工作量。
- 显示未完成的高优先级任务数。
- 指标应随新增、删除、状态变更、导入任务而更新。

### 任务表单

- 表单应包含以下字段：
  - 标题
  - 负责人
  - 工作量
  - 优先级
  - 状态
  - 备注
- 标题为空或只包含空白字符时，不应新增任务。
- 工作量应被归一化为有限、非负数字。
- 优先级应归一化为 `low`、`medium`、`high` 之一。
- 状态应归一化为 `backlog`、`doing`、`review`、`done` 之一。
- 表单控件必须具备可访问 label。

### 搜索和筛选

- 应提供搜索输入框。
- 应提供状态筛选。
- 应提供负责人筛选。
- 搜索和筛选应影响看板中可见任务。
- 筛选条件变化后，空列应显示 empty state。

### 看板列

- 应包含四个状态列：
  - Backlog
  - Doing
  - Review
  - Done
- 每列应通过 `data-status` 标识对应状态。
- 当某列没有可见任务时，应显示简洁空状态。

### 任务卡片

- 卡片应显示：
  - 标题
  - 负责人
  - 工作量
  - 优先级
  - 状态
  - 备注
- 卡片应提供简单控件用于变更状态。
- 卡片应提供删除任务控件。
- 任务变更后应重新渲染看板并更新持久化数据。

### 本地持久化

- 任务应存储在 `localStorage`。
- 存储 key 固定为 `sprint-board-lite.tasks.v1`。
- 仅当 `localStorage` 为空时，才 seed 几个有用的 sample tasks。
- 加载任务时应对数据做归一化，避免无效状态、优先级或工作量破坏界面。

### JSON 导出和导入

- 应提供 JSON 导出控件。
- 应提供 JSON 导入控件和文件输入。
- 导出的 JSON 应能代表当前任务列表。
- 导入时应解析 JSON，并对任务执行归一化。
- 导入失败时应给出简洁反馈，不应破坏现有任务数据。

### JavaScript 可复用函数

`src/app.js` 必须暴露以下 named functions，以便测试和复用：

- `normalizeTask`
- `calculateMetrics`
- `filterTasks`
- `saveTasks`
- `loadTasks`
- `renderBoard`

DOM 启动逻辑必须被保护，保证在非浏览器环境检查模块时不会立即失败。

### 响应式和可访问性

- 桌面端应呈现密集、实用的 dashboard 布局。
- 移动端应保持表单、筛选器、指标和卡片可读可操作。
- 不应出现文字重叠。
- 所有表单控件应有可访问 label。
- 交互元素应有可见 focus 状态。
- UI 文案应简洁，适合工作工具。

## 约束

- 只能使用 plain HTML、CSS、JavaScript。
- 不允许添加 npm、构建工具、远程 CDN、外部字体或框架依赖。
- 不使用外部图片。
- 不使用装饰性渐变。
- 不删除、跳过、弱化或重写现有契约测试。
- 可以添加 focused complementary tests，但不应替代现有契约测试。
- 最终实现应通过：
  - `python3 -m unittest discover -s tests`
- 最终实现阶段还应进行本地手动 smoke test：
  - 添加任务。
  - 移动任务到另一个状态。
  - 使用搜索或筛选。
  - 确认指标更新。
  - 确认导出产生 JSON。

## 步骤

当前需求阶段：

1. 阅读项目目录、现有 scaffold 和契约测试。
2. 判断需求是否依赖现有系统。
3. 生成可确认、可进入设计阶段的需求文档。
4. 不进行设计、任务拆分或代码实现。

后续阶段建议：

1. 设计阶段基于本文档明确页面结构、状态模型、渲染流程、数据归一化规则和导入导出交互。
2. 任务阶段将设计拆解为可执行清单。
3. 实现阶段修改 `index.html`、`src/styles.css`、`src/app.js`，并运行契约测试和手动 smoke test。

## 待确认问题

以下问题不阻塞当前需求文档生成，但建议在设计阶段开始前确认：

1. JSON 导入应替换当前任务列表，还是与现有任务合并？
2. 导入 JSON 的允许格式是否只接受任务数组，还是也接受包含元数据的对象格式？
3. 删除任务是否需要二次确认？
4. 负责人筛选是否只从当前任务负责人自动生成选项？
5. 完成百分比是否按 `done` 任务数量计算，而不是按工作量加权计算？


 succeeded in 0ms:
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

codex
我已经确认两份输入文档存在，设计文档已经给出导入替换、负责人筛选来源、完成百分比算法等决策，因此目前没有阻塞任务划分的问题。接下来补读设计文档末尾，按模块边界生成 `doc/tasks` 文件。
exec
/bin/bash -lc 'find doc/tasks -maxdepth 1 -type f -print 2>/dev/null | sort' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
exec
/bin/bash -lc "sed -n '321,520p' doc/detailed-design.md" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
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

codex
准备写入的模块会严格对应设计文档中的模块边界，并额外放一个验证模块承接契约测试和手动 smoke test，因为需求文档把最终验证作为交付约束。所有文件只会写在 `doc/tasks` 下，不修改业务代码。
exec
/bin/bash -lc 'mkdir -p doc/tasks' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
codex
我将生成 12 个任务文件：11 个实现模块任务，加 1 个验证模块任务。这样实现 agent 可以按模块推进，同时保留每个模块自己的验收和测试清单。
apply patch
patch: completed
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
new file mode 100644
index 0000000000000000000000000000000000000000..4492ef8775d1c928654803af7436c0c471a67919
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
@@ -0,0 +1,51 @@
+# 可访问性模块
+
+## 模块目标
+
+保证 Sprint Board Lite 的表单、筛选器、任务卡片、状态变更、删除、导入导出和反馈区域具备基本键盘可用性和语义可理解性。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 交互控制模块输出
+- 样式和响应式模块输出
+
+## 不做什么
+
+- 不引入额外可访问性库。
+- 不改变已确认的产品规则。
+- 不用颜色作为唯一信息表达方式。
+
+## 任务 checklist
+
+- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
+- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
+- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
+- [ ] 为反馈区域添加 `aria-live="polite"`。
+- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
+- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
+- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
+- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
+- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
+- [ ] 检查移动端控件点击目标和文本可读性。
+
+## 验收标准
+
+- 所有高频交互可通过键盘完成。
+- 所有表单控件和筛选控件可被辅助技术理解。
+- 操作反馈不会只通过视觉位置变化表达。
+- 任务状态和优先级不只依赖颜色。
+
+## 测试要求
+
+- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
+- [ ] 人工检查 label 与控件 id 的关联。
+- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
+- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
+
+## 风险和注意事项
+
+- 动态创建卡片时容易遗漏控件 label 或可访问名称，应在渲染函数中统一生成。
+- focus 样式不能被全局 reset 或低对比度颜色覆盖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
new file mode 100644
index 0000000000000000000000000000000000000000..a533ed9f26d917675e91724bdb0a4d5a85624d5c
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
@@ -0,0 +1,54 @@
+# 看板渲染模块
+
+## 模块目标
+
+实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 指标计算模块输出
+- 筛选模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不绑定全局启动事件。
+- 不直接读取表单输入。
+- 不直接解析 JSON 文件。
+
+## 任务 checklist
+
+- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
+- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
+- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
+- [ ] 使用 `filterTasks` 计算可见任务。
+- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
+- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
+- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为每个任务卡片创建状态变更控件。
+- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
+- [ ] 为没有可见任务的列插入简洁 empty state。
+- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
+- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
+
+## 验收标准
+
+- 所有任务变更后重渲染不会产生重复卡片。
+- KPI 始终显示完整任务列表指标。
+- 空列显示 empty state。
+- 卡片包含需求文档列出的所有任务字段。
+- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `renderBoard` 存在。
+- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
+- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
+
+## 风险和注意事项
+
+- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
+- 重建 owner 选项时不要错误清空用户当前有效筛选值。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
new file mode 100644
index 0000000000000000000000000000000000000000..f164a168dc9e1382dae45a34fd84ac8119bdfb70
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
@@ -0,0 +1,47 @@
+# 数据模型模块
+
+## 模块目标
+
+定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- `src/app.js`
+
+## 不做什么
+
+- 不直接操作 DOM。
+- 不直接读写 `localStorage`。
+- 不实现筛选、指标计算或 JSON 导入导出。
+
+## 任务 checklist
+
+- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
+- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
+- [ ] 定义优先级集合：`low`、`medium`、`high`。
+- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
+- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
+- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
+- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
+- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
+- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
+- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
+
+## 验收标准
+
+- 数据结构与设计文档中的任务对象一致。
+- 状态、优先级和筛选默认值可被后续模块复用。
+- 存储 key 固定且只定义一处。
+- 模块加载时不会因为缺少浏览器 API 报错。
+
+## 测试要求
+
+- [ ] 使用契约测试确认固定存储 key 仍符合要求。
+- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
+
+## 风险和注意事项
+
+- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
+- 显示文案可以变化，但内部值不可随意变化。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
new file mode 100644
index 0000000000000000000000000000000000000000..386f69f51e872994f3adf1b145b70cbb9fa34c44
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
@@ -0,0 +1,50 @@
+# 筛选模块
+
+## 模块目标
+
+实现 `filterTasks` 和负责人筛选选项生成规则，让搜索、状态筛选和负责人筛选影响看板可见任务，同时不改变完整任务列表。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不计算 KPI。
+- 不读写 `localStorage`。
+- 不删除或修改任务数据。
+
+## 任务 checklist
+
+- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
+- [ ] 支持 `query` 关键词搜索，大小写不敏感。
+- [ ] 让关键词至少匹配标题、负责人和备注。
+- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
+- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
+- [ ] 将搜索、状态和负责人筛选条件组合为交集。
+- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
+- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
+- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
+- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
+
+## 验收标准
+
+- 搜索和筛选只影响可见任务，不改变 `appState.tasks`。
+- 筛选无结果时四个看板列仍然存在。
+- 负责人筛选选项不会从当前搜索结果派生，而是从完整任务列表派生。
+- 删除某负责人最后一个任务后，失效 owner 筛选会回退到 `All`。
+
+## 测试要求
+
+- [ ] 验证关键词匹配标题、负责人和备注。
+- [ ] 验证状态筛选、负责人筛选和组合筛选。
+- [ ] 验证大小写不敏感搜索。
+- [ ] 验证 owner 选项去重和 `All` 首项规则。
+
+## 风险和注意事项
+
+- `filterTasks` 应保持纯函数，不要在其中修改 filters。
+- owner 失效回退可以由渲染或交互模块处理，但必须在重渲染前生效。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
new file mode 100644
index 0000000000000000000000000000000000000000..9a3b3ec627842583b96e7e7ef5eb7cd2af18cc98
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
@@ -0,0 +1,56 @@
+# 交互控制模块
+
+## 模块目标
+
+实现 DOM 启动保护、应用状态初始化和事件绑定，让新增、搜索、筛选、状态变更、删除等核心交互按设计数据流运行。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 归一化、持久化、筛选、渲染模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不实现 JSON 文件解析和 Blob 下载细节。
+- 不新增后端或异步服务。
+- 不弹出删除二次确认。
+
+## 任务 checklist
+
+- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
+- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
+- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
+- [ ] 绑定任务表单提交事件。
+- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
+- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
+- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
+- [ ] 新增成功后清理表单到可继续录入状态。
+- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
+- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
+- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
+- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
+- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
+- [ ] 删除任务时不弹二次确认。
+- [ ] 所有操作反馈写入统一反馈区域。
+
+## 验收标准
+
+- 模块在非浏览器环境加载不会失败。
+- 新增有效任务后任务出现在对应状态列，KPI 和存储同步更新。
+- 空标题提交不会新增任务。
+- 搜索和筛选改变可见任务，但不写入存储。
+- 卡片状态变更和删除能准确定位对应任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
+- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
+- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
+
+## 风险和注意事项
+
+- 事件绑定只应初始化一次，避免多次 render 后重复触发。
+- 任务状态更新后必须经过保存和重渲染，不能只改 DOM。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
new file mode 100644
index 0000000000000000000000000000000000000000..c8c471f1bfa250c2a130c18870b3c143eb8e9931
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
@@ -0,0 +1,59 @@
+# JSON 导入导出模块
+
+## 模块目标
+
+实现当前完整任务列表的 JSON 导出，以及任务数组或 `{ "tasks": [...] }` 对象格式的原子导入替换。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 归一化模块输出
+- 持久化模块输出
+- 渲染模块输出
+- 交互控制模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不合并导入任务和当前任务。
+- 不接受设计文档之外的导入格式。
+- 不在导入失败时覆盖当前任务数据。
+
+## 任务 checklist
+
+- [ ] 绑定 JSON 导出按钮事件。
+- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
+- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
+- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
+- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
+- [ ] 绑定 JSON 导入控件或文件输入事件。
+- [ ] 读取导入文件文本并执行 `JSON.parse`。
+- [ ] 接受任务数组格式：`[{...}, {...}]`。
+- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
+- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
+- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
+- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
+- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
+- [ ] 导入空数组时视为合法导入，替换为无任务状态。
+- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
+
+## 验收标准
+
+- 导出 JSON 表示完整任务列表。
+- 导入任务数组会替换当前任务列表。
+- 导入 `{ "tasks": [...] }` 会替换当前任务列表。
+- 非法 JSON、合法 JSON 但格式错误、`tasks` 非数组都不会覆盖当前数据。
+- 成功导入后 KPI、看板、负责人筛选和 `localStorage` 同步更新。
+
+## 测试要求
+
+- [ ] 人工验证导出文件内容包含完整任务列表。
+- [ ] 验证数组导入、对象导入、空数组导入。
+- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
+- [ ] 验证导入失败后现有任务仍保留。
+
+## 风险和注意事项
+
+- 导入替换必须是原子性的，不能边解析边覆盖当前状态。
+- 导出下载链接创建后应及时清理，避免 DOM 残留。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
new file mode 100644
index 0000000000000000000000000000000000000000..c477d58b4f86906322d8992ac0fb15bb72e561be
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
@@ -0,0 +1,48 @@
+# 指标计算模块
+
+## 模块目标
+
+实现 `calculateMetrics`，基于完整任务列表计算 KPI：总任务数、完成百分比、总工作量、未完成高优先级任务数。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读取筛选条件。
+- 不操作 DOM。
+- 不读写 `localStorage`。
+
+## 任务 checklist
+
+- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
+- [ ] 计算总任务数为完整任务数组长度。
+- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
+- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
+- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
+- [ ] 计算总工作量为所有任务 `effort` 求和。
+- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
+- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
+- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
+
+## 验收标准
+
+- 空任务列表返回总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`。
+- 全部任务完成时完成百分比为 `100%`。
+- 完成百分比按任务数量计算，不按工作量加权。
+- 筛选条件改变时 KPI 仍反映完整任务列表。
+
+## 测试要求
+
+- [ ] 验证空列表、部分完成、全部完成三种场景。
+- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
+- [ ] 验证工作量求和使用归一化后的数字。
+
+## 风险和注意事项
+
+- KPI 显示格式由渲染模块决定，计算模块应优先返回数值，避免字符串格式耦合。
+- 不要把筛选后的可见任务误传给 `calculateMetrics`。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
new file mode 100644
index 0000000000000000000000000000000000000000..549ae805a0ee8fd5425f6300cd192b965c387648
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
@@ -0,0 +1,49 @@
+# 数据归一化模块
+
+## 模块目标
+
+实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读写 DOM。
+- 不读写 `localStorage`。
+- 不决定任务是否保存或渲染。
+
+## 任务 checklist
+
+- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
+- [ ] 将 `title` 转为字符串并 trim。
+- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
+- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
+- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
+- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
+- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
+- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
+- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
+- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
+
+## 验收标准
+
+- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
+- 归一化函数不产生 DOM 或存储副作用。
+- 空标题任务不会被新增、导入或从存储中恢复到看板。
+- 无效状态、优先级和工作量不会破坏界面。
+
+## 测试要求
+
+- [ ] 补充或运行测试覆盖有效任务归一化。
+- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
+- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
+
+## 风险和注意事项
+
+- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
+- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
new file mode 100644
index 0000000000000000000000000000000000000000..b94aa88fa29ef4f691f0e06445950b9776216711
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
@@ -0,0 +1,49 @@
+# 页面结构模块
+
+## 模块目标
+
+实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 现有 `index.html`
+- 现有契约测试声明的必要元素 id、文本和 selector
+
+## 不做什么
+
+- 不实现业务逻辑、状态管理或数据持久化。
+- 不引入框架、CDN、外部字体、图片或构建工具。
+- 不创建营销 landing page。
+
+## 任务 checklist
+
+- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
+- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
+- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
+- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
+- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
+- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
+- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
+- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
+- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
+- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
+
+## 验收标准
+
+- 页面不是营销页，首屏包含实际工作看板。
+- 四个状态列都存在，并使用正确的 `data-status` 值。
+- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
+- 所有表单控件具备可访问 label。
+- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
+- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。
+
+## 风险和注意事项
+
+- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
+- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
new file mode 100644
index 0000000000000000000000000000000000000000..8e0fae9b4d5e54500e64efe9ed6f98d49e304c95
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
@@ -0,0 +1,50 @@
+# 持久化模块
+
+## 模块目标
+
+实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- 数据归一化模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不渲染 DOM。
+- 不处理筛选条件。
+- 不实现 JSON 文件导入导出。
+
+## 任务 checklist
+
+- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
+- [ ] 在保存前确保写入的是可序列化任务数组。
+- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
+- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
+- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
+- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
+- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
+- [ ] 对读取到的每条任务执行 `normalizeTask`。
+- [ ] 过滤空标题任务，避免无效任务进入应用状态。
+- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
+
+## 验收标准
+
+- 首次打开且无固定 key 时出现 sample tasks。
+- 固定 key 存在为空数组时，看板保持空任务状态。
+- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
+- 保存、新增、删除、状态变更和导入后使用同一个固定 key。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
+- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
+- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
+
+## 风险和注意事项
+
+- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
+- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
new file mode 100644
index 0000000000000000000000000000000000000000..f27641ce8a850b4b51d956870c59b07e95ebe05a
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
@@ -0,0 +1,56 @@
+# Sprint Board Lite 总体任务进度
+
+## 目标
+
+基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。
+
+## 模块进度
+
+- [ ] 页面结构模块：`doc/tasks/page-structure.md`
+- [ ] 数据模型模块：`doc/tasks/data-model.md`
+- [ ] 数据归一化模块：`doc/tasks/normalization.md`
+- [ ] 持久化模块：`doc/tasks/persistence.md`
+- [ ] 指标计算模块：`doc/tasks/metrics.md`
+- [ ] 筛选模块：`doc/tasks/filtering.md`
+- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
+- [ ] 交互控制模块：`doc/tasks/interactions.md`
+- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
+- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
+- [ ] 可访问性模块：`doc/tasks/accessibility.md`
+- [ ] 验证模块：`doc/tasks/verification.md`
+
+## 推荐执行顺序
+
+1. 页面结构模块
+2. 数据模型模块
+3. 数据归一化模块
+4. 持久化模块
+5. 指标计算模块
+6. 筛选模块
+7. 看板渲染模块
+8. 交互控制模块
+9. JSON 导入导出模块
+10. 样式和响应式模块
+11. 可访问性模块
+12. 验证模块
+
+## 可并行项
+
+- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
+- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
+- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
+- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
+
+## 阻塞项
+
+- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
+
+## 跨模块注意事项
+
+- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
+- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
+- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
+- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
+- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
+- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
+- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ca3e699d07ce48175fe50897f5ecc10978bedc5
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
@@ -0,0 +1,54 @@
+# 样式和响应式模块
+
+## 模块目标
+
+实现安静、密集、实用的 dashboard 工具界面，并保证桌面和移动端下 KPI、表单、筛选器、看板列和任务卡片可读可操作。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 看板渲染模块输出
+- `src/styles.css`
+
+## 不做什么
+
+- 不使用外部字体、图片、CDN、框架或装饰性渐变。
+- 不制作营销页视觉。
+- 不用 viewport width 直接缩放字体。
+
+## 任务 checklist
+
+- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
+- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
+- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
+- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
+- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
+- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
+- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
+- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
+- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
+- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
+- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
+
+## 验收标准
+
+- 桌面端页面密集、清晰、适合重复操作。
+- 移动端文本不重叠，表单和卡片可操作。
+- 看板列、卡片和控件尺寸稳定。
+- UI 不依赖外部资源。
+- 页面没有装饰性渐变、外部图片或 landing page 构图。
+
+## 测试要求
+
+- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
+- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
+- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
+- [ ] 验证键盘 focus 状态清晰可见。
+
+## 风险和注意事项
+
+- 颜色系统应服务状态识别，不要让页面变成单一色调。
+- 样式不能隐藏契约测试要求的文本或元素。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
new file mode 100644
index 0000000000000000000000000000000000000000..c0b96b74833e7c4c760885681c4bb8680b5c9c51
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
@@ -0,0 +1,57 @@
+# 验证模块
+
+## 模块目标
+
+在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 所有实现模块输出
+- `tests/test_static_contract.py`
+
+## 不做什么
+
+- 不跳过、删除、弱化或重写现有契约测试。
+- 不用补充测试替代契约测试。
+- 不引入自动化测试框架或构建工具。
+
+## 任务 checklist
+
+- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
+- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
+- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
+- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
+- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
+- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
+- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
+- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
+- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
+- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
+- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
+- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
+- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
+- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
+- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
+- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
+
+## 验收标准
+
+- 契约测试全部通过。
+- 需求文档列出的最终手动 smoke test 全部通过。
+- 设计文档列出的边界情况至少完成人工或自动验证。
+- 不存在业务代码之外的无关修改。
+
+## 测试要求
+
+- [ ] 必须执行 `python3 -m unittest discover -s tests`。
+- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
+- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
+
+## 风险和注意事项
+
+- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
+- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。

diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
new file mode 100644
index 0000000000000000000000000000000000000000..4492ef8775d1c928654803af7436c0c471a67919
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
@@ -0,0 +1,51 @@
+# 可访问性模块
+
+## 模块目标
+
+保证 Sprint Board Lite 的表单、筛选器、任务卡片、状态变更、删除、导入导出和反馈区域具备基本键盘可用性和语义可理解性。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 交互控制模块输出
+- 样式和响应式模块输出
+
+## 不做什么
+
+- 不引入额外可访问性库。
+- 不改变已确认的产品规则。
+- 不用颜色作为唯一信息表达方式。
+
+## 任务 checklist
+
+- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
+- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
+- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
+- [ ] 为反馈区域添加 `aria-live="polite"`。
+- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
+- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
+- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
+- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
+- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
+- [ ] 检查移动端控件点击目标和文本可读性。
+
+## 验收标准
+
+- 所有高频交互可通过键盘完成。
+- 所有表单控件和筛选控件可被辅助技术理解。
+- 操作反馈不会只通过视觉位置变化表达。
+- 任务状态和优先级不只依赖颜色。
+
+## 测试要求
+
+- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
+- [ ] 人工检查 label 与控件 id 的关联。
+- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
+- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
+
+## 风险和注意事项
+
+- 动态创建卡片时容易遗漏控件 label 或可访问名称，应在渲染函数中统一生成。
+- focus 样式不能被全局 reset 或低对比度颜色覆盖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
new file mode 100644
index 0000000000000000000000000000000000000000..a533ed9f26d917675e91724bdb0a4d5a85624d5c
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
@@ -0,0 +1,54 @@
+# 看板渲染模块
+
+## 模块目标
+
+实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 指标计算模块输出
+- 筛选模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不绑定全局启动事件。
+- 不直接读取表单输入。
+- 不直接解析 JSON 文件。
+
+## 任务 checklist
+
+- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
+- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
+- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
+- [ ] 使用 `filterTasks` 计算可见任务。
+- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
+- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
+- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为每个任务卡片创建状态变更控件。
+- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
+- [ ] 为没有可见任务的列插入简洁 empty state。
+- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
+- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
+
+## 验收标准
+
+- 所有任务变更后重渲染不会产生重复卡片。
+- KPI 始终显示完整任务列表指标。
+- 空列显示 empty state。
+- 卡片包含需求文档列出的所有任务字段。
+- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `renderBoard` 存在。
+- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
+- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
+
+## 风险和注意事项
+
+- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
+- 重建 owner 选项时不要错误清空用户当前有效筛选值。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
new file mode 100644
index 0000000000000000000000000000000000000000..f164a168dc9e1382dae45a34fd84ac8119bdfb70
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
@@ -0,0 +1,47 @@
+# 数据模型模块
+
+## 模块目标
+
+定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- `src/app.js`
+
+## 不做什么
+
+- 不直接操作 DOM。
+- 不直接读写 `localStorage`。
+- 不实现筛选、指标计算或 JSON 导入导出。
+
+## 任务 checklist
+
+- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
+- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
+- [ ] 定义优先级集合：`low`、`medium`、`high`。
+- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
+- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
+- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
+- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
+- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
+- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
+- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
+
+## 验收标准
+
+- 数据结构与设计文档中的任务对象一致。
+- 状态、优先级和筛选默认值可被后续模块复用。
+- 存储 key 固定且只定义一处。
+- 模块加载时不会因为缺少浏览器 API 报错。
+
+## 测试要求
+
+- [ ] 使用契约测试确认固定存储 key 仍符合要求。
+- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
+
+## 风险和注意事项
+
+- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
+- 显示文案可以变化，但内部值不可随意变化。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
new file mode 100644
index 0000000000000000000000000000000000000000..386f69f51e872994f3adf1b145b70cbb9fa34c44
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
@@ -0,0 +1,50 @@
+# 筛选模块
+
+## 模块目标
+
+实现 `filterTasks` 和负责人筛选选项生成规则，让搜索、状态筛选和负责人筛选影响看板可见任务，同时不改变完整任务列表。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不计算 KPI。
+- 不读写 `localStorage`。
+- 不删除或修改任务数据。
+
+## 任务 checklist
+
+- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
+- [ ] 支持 `query` 关键词搜索，大小写不敏感。
+- [ ] 让关键词至少匹配标题、负责人和备注。
+- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
+- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
+- [ ] 将搜索、状态和负责人筛选条件组合为交集。
+- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
+- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
+- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
+- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
+
+## 验收标准
+
+- 搜索和筛选只影响可见任务，不改变 `appState.tasks`。
+- 筛选无结果时四个看板列仍然存在。
+- 负责人筛选选项不会从当前搜索结果派生，而是从完整任务列表派生。
+- 删除某负责人最后一个任务后，失效 owner 筛选会回退到 `All`。
+
+## 测试要求
+
+- [ ] 验证关键词匹配标题、负责人和备注。
+- [ ] 验证状态筛选、负责人筛选和组合筛选。
+- [ ] 验证大小写不敏感搜索。
+- [ ] 验证 owner 选项去重和 `All` 首项规则。
+
+## 风险和注意事项
+
+- `filterTasks` 应保持纯函数，不要在其中修改 filters。
+- owner 失效回退可以由渲染或交互模块处理，但必须在重渲染前生效。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
new file mode 100644
index 0000000000000000000000000000000000000000..9a3b3ec627842583b96e7e7ef5eb7cd2af18cc98
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
@@ -0,0 +1,56 @@
+# 交互控制模块
+
+## 模块目标
+
+实现 DOM 启动保护、应用状态初始化和事件绑定，让新增、搜索、筛选、状态变更、删除等核心交互按设计数据流运行。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 归一化、持久化、筛选、渲染模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不实现 JSON 文件解析和 Blob 下载细节。
+- 不新增后端或异步服务。
+- 不弹出删除二次确认。
+
+## 任务 checklist
+
+- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
+- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
+- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
+- [ ] 绑定任务表单提交事件。
+- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
+- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
+- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
+- [ ] 新增成功后清理表单到可继续录入状态。
+- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
+- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
+- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
+- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
+- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
+- [ ] 删除任务时不弹二次确认。
+- [ ] 所有操作反馈写入统一反馈区域。
+
+## 验收标准
+
+- 模块在非浏览器环境加载不会失败。
+- 新增有效任务后任务出现在对应状态列，KPI 和存储同步更新。
+- 空标题提交不会新增任务。
+- 搜索和筛选改变可见任务，但不写入存储。
+- 卡片状态变更和删除能准确定位对应任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
+- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
+- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
+
+## 风险和注意事项
+
+- 事件绑定只应初始化一次，避免多次 render 后重复触发。
+- 任务状态更新后必须经过保存和重渲染，不能只改 DOM。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
new file mode 100644
index 0000000000000000000000000000000000000000..c8c471f1bfa250c2a130c18870b3c143eb8e9931
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
@@ -0,0 +1,59 @@
+# JSON 导入导出模块
+
+## 模块目标
+
+实现当前完整任务列表的 JSON 导出，以及任务数组或 `{ "tasks": [...] }` 对象格式的原子导入替换。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 归一化模块输出
+- 持久化模块输出
+- 渲染模块输出
+- 交互控制模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不合并导入任务和当前任务。
+- 不接受设计文档之外的导入格式。
+- 不在导入失败时覆盖当前任务数据。
+
+## 任务 checklist
+
+- [ ] 绑定 JSON 导出按钮事件。
+- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
+- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
+- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
+- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
+- [ ] 绑定 JSON 导入控件或文件输入事件。
+- [ ] 读取导入文件文本并执行 `JSON.parse`。
+- [ ] 接受任务数组格式：`[{...}, {...}]`。
+- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
+- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
+- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
+- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
+- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
+- [ ] 导入空数组时视为合法导入，替换为无任务状态。
+- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
+
+## 验收标准
+
+- 导出 JSON 表示完整任务列表。
+- 导入任务数组会替换当前任务列表。
+- 导入 `{ "tasks": [...] }` 会替换当前任务列表。
+- 非法 JSON、合法 JSON 但格式错误、`tasks` 非数组都不会覆盖当前数据。
+- 成功导入后 KPI、看板、负责人筛选和 `localStorage` 同步更新。
+
+## 测试要求
+
+- [ ] 人工验证导出文件内容包含完整任务列表。
+- [ ] 验证数组导入、对象导入、空数组导入。
+- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
+- [ ] 验证导入失败后现有任务仍保留。
+
+## 风险和注意事项
+
+- 导入替换必须是原子性的，不能边解析边覆盖当前状态。
+- 导出下载链接创建后应及时清理，避免 DOM 残留。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
new file mode 100644
index 0000000000000000000000000000000000000000..c477d58b4f86906322d8992ac0fb15bb72e561be
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
@@ -0,0 +1,48 @@
+# 指标计算模块
+
+## 模块目标
+
+实现 `calculateMetrics`，基于完整任务列表计算 KPI：总任务数、完成百分比、总工作量、未完成高优先级任务数。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读取筛选条件。
+- 不操作 DOM。
+- 不读写 `localStorage`。
+
+## 任务 checklist
+
+- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
+- [ ] 计算总任务数为完整任务数组长度。
+- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
+- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
+- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
+- [ ] 计算总工作量为所有任务 `effort` 求和。
+- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
+- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
+- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
+
+## 验收标准
+
+- 空任务列表返回总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`。
+- 全部任务完成时完成百分比为 `100%`。
+- 完成百分比按任务数量计算，不按工作量加权。
+- 筛选条件改变时 KPI 仍反映完整任务列表。
+
+## 测试要求
+
+- [ ] 验证空列表、部分完成、全部完成三种场景。
+- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
+- [ ] 验证工作量求和使用归一化后的数字。
+
+## 风险和注意事项
+
+- KPI 显示格式由渲染模块决定，计算模块应优先返回数值，避免字符串格式耦合。
+- 不要把筛选后的可见任务误传给 `calculateMetrics`。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
new file mode 100644
index 0000000000000000000000000000000000000000..549ae805a0ee8fd5425f6300cd192b965c387648
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
@@ -0,0 +1,49 @@
+# 数据归一化模块
+
+## 模块目标
+
+实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读写 DOM。
+- 不读写 `localStorage`。
+- 不决定任务是否保存或渲染。
+
+## 任务 checklist
+
+- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
+- [ ] 将 `title` 转为字符串并 trim。
+- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
+- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
+- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
+- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
+- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
+- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
+- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
+- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
+
+## 验收标准
+
+- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
+- 归一化函数不产生 DOM 或存储副作用。
+- 空标题任务不会被新增、导入或从存储中恢复到看板。
+- 无效状态、优先级和工作量不会破坏界面。
+
+## 测试要求
+
+- [ ] 补充或运行测试覆盖有效任务归一化。
+- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
+- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
+
+## 风险和注意事项
+
+- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
+- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
new file mode 100644
index 0000000000000000000000000000000000000000..b94aa88fa29ef4f691f0e06445950b9776216711
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
@@ -0,0 +1,49 @@
+# 页面结构模块
+
+## 模块目标
+
+实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 现有 `index.html`
+- 现有契约测试声明的必要元素 id、文本和 selector
+
+## 不做什么
+
+- 不实现业务逻辑、状态管理或数据持久化。
+- 不引入框架、CDN、外部字体、图片或构建工具。
+- 不创建营销 landing page。
+
+## 任务 checklist
+
+- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
+- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
+- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
+- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
+- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
+- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
+- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
+- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
+- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
+- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
+
+## 验收标准
+
+- 页面不是营销页，首屏包含实际工作看板。
+- 四个状态列都存在，并使用正确的 `data-status` 值。
+- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
+- 所有表单控件具备可访问 label。
+- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
+- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。
+
+## 风险和注意事项
+
+- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
+- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
new file mode 100644
index 0000000000000000000000000000000000000000..8e0fae9b4d5e54500e64efe9ed6f98d49e304c95
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
@@ -0,0 +1,50 @@
+# 持久化模块
+
+## 模块目标
+
+实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- 数据归一化模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不渲染 DOM。
+- 不处理筛选条件。
+- 不实现 JSON 文件导入导出。
+
+## 任务 checklist
+
+- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
+- [ ] 在保存前确保写入的是可序列化任务数组。
+- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
+- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
+- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
+- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
+- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
+- [ ] 对读取到的每条任务执行 `normalizeTask`。
+- [ ] 过滤空标题任务，避免无效任务进入应用状态。
+- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
+
+## 验收标准
+
+- 首次打开且无固定 key 时出现 sample tasks。
+- 固定 key 存在为空数组时，看板保持空任务状态。
+- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
+- 保存、新增、删除、状态变更和导入后使用同一个固定 key。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
+- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
+- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
+
+## 风险和注意事项
+
+- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
+- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
new file mode 100644
index 0000000000000000000000000000000000000000..f27641ce8a850b4b51d956870c59b07e95ebe05a
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
@@ -0,0 +1,56 @@
+# Sprint Board Lite 总体任务进度
+
+## 目标
+
+基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。
+
+## 模块进度
+
+- [ ] 页面结构模块：`doc/tasks/page-structure.md`
+- [ ] 数据模型模块：`doc/tasks/data-model.md`
+- [ ] 数据归一化模块：`doc/tasks/normalization.md`
+- [ ] 持久化模块：`doc/tasks/persistence.md`
+- [ ] 指标计算模块：`doc/tasks/metrics.md`
+- [ ] 筛选模块：`doc/tasks/filtering.md`
+- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
+- [ ] 交互控制模块：`doc/tasks/interactions.md`
+- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
+- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
+- [ ] 可访问性模块：`doc/tasks/accessibility.md`
+- [ ] 验证模块：`doc/tasks/verification.md`
+
+## 推荐执行顺序
+
+1. 页面结构模块
+2. 数据模型模块
+3. 数据归一化模块
+4. 持久化模块
+5. 指标计算模块
+6. 筛选模块
+7. 看板渲染模块
+8. 交互控制模块
+9. JSON 导入导出模块
+10. 样式和响应式模块
+11. 可访问性模块
+12. 验证模块
+
+## 可并行项
+
+- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
+- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
+- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
+- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
+
+## 阻塞项
+
+- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
+
+## 跨模块注意事项
+
+- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
+- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
+- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
+- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
+- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
+- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
+- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ca3e699d07ce48175fe50897f5ecc10978bedc5
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
@@ -0,0 +1,54 @@
+# 样式和响应式模块
+
+## 模块目标
+
+实现安静、密集、实用的 dashboard 工具界面，并保证桌面和移动端下 KPI、表单、筛选器、看板列和任务卡片可读可操作。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 看板渲染模块输出
+- `src/styles.css`
+
+## 不做什么
+
+- 不使用外部字体、图片、CDN、框架或装饰性渐变。
+- 不制作营销页视觉。
+- 不用 viewport width 直接缩放字体。
+
+## 任务 checklist
+
+- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
+- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
+- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
+- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
+- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
+- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
+- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
+- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
+- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
+- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
+- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
+
+## 验收标准
+
+- 桌面端页面密集、清晰、适合重复操作。
+- 移动端文本不重叠，表单和卡片可操作。
+- 看板列、卡片和控件尺寸稳定。
+- UI 不依赖外部资源。
+- 页面没有装饰性渐变、外部图片或 landing page 构图。
+
+## 测试要求
+
+- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
+- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
+- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
+- [ ] 验证键盘 focus 状态清晰可见。
+
+## 风险和注意事项
+
+- 颜色系统应服务状态识别，不要让页面变成单一色调。
+- 样式不能隐藏契约测试要求的文本或元素。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
new file mode 100644
index 0000000000000000000000000000000000000000..c0b96b74833e7c4c760885681c4bb8680b5c9c51
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
@@ -0,0 +1,57 @@
+# 验证模块
+
+## 模块目标
+
+在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 所有实现模块输出
+- `tests/test_static_contract.py`
+
+## 不做什么
+
+- 不跳过、删除、弱化或重写现有契约测试。
+- 不用补充测试替代契约测试。
+- 不引入自动化测试框架或构建工具。
+
+## 任务 checklist
+
+- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
+- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
+- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
+- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
+- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
+- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
+- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
+- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
+- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
+- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
+- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
+- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
+- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
+- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
+- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
+- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
+
+## 验收标准
+
+- 契约测试全部通过。
+- 需求文档列出的最终手动 smoke test 全部通过。
+- 设计文档列出的边界情况至少完成人工或自动验证。
+- 不存在业务代码之外的无关修改。
+
+## 测试要求
+
+- [ ] 必须执行 `python3 -m unittest discover -s tests`。
+- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
+- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
+
+## 风险和注意事项
+
+- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
+- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。

codex
`doc/tasks` 已经写入。现在做一次结构核对，确认模块文件齐全、没有触碰业务代码，并检查任务清单格式。
exec
/bin/bash -lc 'rg -n "''^- '"\\[[ x]\\]\" doc/tasks" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 exited 127 in 0ms:
/bin/bash: rg: command not found

exec
/bin/bash -lc 'find doc/tasks -maxdepth 1 -type f -print | sort' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
doc/tasks/accessibility.md
doc/tasks/board-rendering.md
doc/tasks/data-model.md
doc/tasks/filtering.md
doc/tasks/interactions.md
doc/tasks/json-import-export.md
doc/tasks/metrics.md
doc/tasks/normalization.md
doc/tasks/page-structure.md
doc/tasks/persistence.md
doc/tasks/progress.md
doc/tasks/styles-responsive.md
doc/tasks/verification.md

exec
/bin/bash -lc 'git status --short' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
?? ../../../.DS_Store
?? ../../../doc/
?? ../../

exec
/bin/bash -lc 'wc -l doc/tasks/*.md' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
      51 doc/tasks/accessibility.md
      54 doc/tasks/board-rendering.md
      47 doc/tasks/data-model.md
      50 doc/tasks/filtering.md
      56 doc/tasks/interactions.md
      59 doc/tasks/json-import-export.md
      48 doc/tasks/metrics.md
      49 doc/tasks/normalization.md
      49 doc/tasks/page-structure.md
      50 doc/tasks/persistence.md
      56 doc/tasks/progress.md
      54 doc/tasks/styles-responsive.md
      57 doc/tasks/verification.md
     680 total

diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
new file mode 100644
index 0000000000000000000000000000000000000000..4492ef8775d1c928654803af7436c0c471a67919
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
@@ -0,0 +1,51 @@
+# 可访问性模块
+
+## 模块目标
+
+保证 Sprint Board Lite 的表单、筛选器、任务卡片、状态变更、删除、导入导出和反馈区域具备基本键盘可用性和语义可理解性。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 交互控制模块输出
+- 样式和响应式模块输出
+
+## 不做什么
+
+- 不引入额外可访问性库。
+- 不改变已确认的产品规则。
+- 不用颜色作为唯一信息表达方式。
+
+## 任务 checklist
+
+- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
+- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
+- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
+- [ ] 为反馈区域添加 `aria-live="polite"`。
+- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
+- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
+- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
+- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
+- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
+- [ ] 检查移动端控件点击目标和文本可读性。
+
+## 验收标准
+
+- 所有高频交互可通过键盘完成。
+- 所有表单控件和筛选控件可被辅助技术理解。
+- 操作反馈不会只通过视觉位置变化表达。
+- 任务状态和优先级不只依赖颜色。
+
+## 测试要求
+
+- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
+- [ ] 人工检查 label 与控件 id 的关联。
+- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
+- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
+
+## 风险和注意事项
+
+- 动态创建卡片时容易遗漏控件 label 或可访问名称，应在渲染函数中统一生成。
+- focus 样式不能被全局 reset 或低对比度颜色覆盖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
new file mode 100644
index 0000000000000000000000000000000000000000..a533ed9f26d917675e91724bdb0a4d5a85624d5c
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
@@ -0,0 +1,54 @@
+# 看板渲染模块
+
+## 模块目标
+
+实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 指标计算模块输出
+- 筛选模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不绑定全局启动事件。
+- 不直接读取表单输入。
+- 不直接解析 JSON 文件。
+
+## 任务 checklist
+
+- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
+- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
+- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
+- [ ] 使用 `filterTasks` 计算可见任务。
+- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
+- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
+- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为每个任务卡片创建状态变更控件。
+- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
+- [ ] 为没有可见任务的列插入简洁 empty state。
+- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
+- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
+
+## 验收标准
+
+- 所有任务变更后重渲染不会产生重复卡片。
+- KPI 始终显示完整任务列表指标。
+- 空列显示 empty state。
+- 卡片包含需求文档列出的所有任务字段。
+- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `renderBoard` 存在。
+- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
+- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
+
+## 风险和注意事项
+
+- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
+- 重建 owner 选项时不要错误清空用户当前有效筛选值。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
new file mode 100644
index 0000000000000000000000000000000000000000..f164a168dc9e1382dae45a34fd84ac8119bdfb70
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
@@ -0,0 +1,47 @@
+# 数据模型模块
+
+## 模块目标
+
+定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- `src/app.js`
+
+## 不做什么
+
+- 不直接操作 DOM。
+- 不直接读写 `localStorage`。
+- 不实现筛选、指标计算或 JSON 导入导出。
+
+## 任务 checklist
+
+- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
+- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
+- [ ] 定义优先级集合：`low`、`medium`、`high`。
+- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
+- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
+- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
+- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
+- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
+- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
+- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
+
+## 验收标准
+
+- 数据结构与设计文档中的任务对象一致。
+- 状态、优先级和筛选默认值可被后续模块复用。
+- 存储 key 固定且只定义一处。
+- 模块加载时不会因为缺少浏览器 API 报错。
+
+## 测试要求
+
+- [ ] 使用契约测试确认固定存储 key 仍符合要求。
+- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
+
+## 风险和注意事项
+
+- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
+- 显示文案可以变化，但内部值不可随意变化。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
new file mode 100644
index 0000000000000000000000000000000000000000..386f69f51e872994f3adf1b145b70cbb9fa34c44
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
@@ -0,0 +1,50 @@
+# 筛选模块
+
+## 模块目标
+
+实现 `filterTasks` 和负责人筛选选项生成规则，让搜索、状态筛选和负责人筛选影响看板可见任务，同时不改变完整任务列表。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不计算 KPI。
+- 不读写 `localStorage`。
+- 不删除或修改任务数据。
+
+## 任务 checklist
+
+- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
+- [ ] 支持 `query` 关键词搜索，大小写不敏感。
+- [ ] 让关键词至少匹配标题、负责人和备注。
+- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
+- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
+- [ ] 将搜索、状态和负责人筛选条件组合为交集。
+- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
+- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
+- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
+- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
+
+## 验收标准
+
+- 搜索和筛选只影响可见任务，不改变 `appState.tasks`。
+- 筛选无结果时四个看板列仍然存在。
+- 负责人筛选选项不会从当前搜索结果派生，而是从完整任务列表派生。
+- 删除某负责人最后一个任务后，失效 owner 筛选会回退到 `All`。
+
+## 测试要求
+
+- [ ] 验证关键词匹配标题、负责人和备注。
+- [ ] 验证状态筛选、负责人筛选和组合筛选。
+- [ ] 验证大小写不敏感搜索。
+- [ ] 验证 owner 选项去重和 `All` 首项规则。
+
+## 风险和注意事项
+
+- `filterTasks` 应保持纯函数，不要在其中修改 filters。
+- owner 失效回退可以由渲染或交互模块处理，但必须在重渲染前生效。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
new file mode 100644
index 0000000000000000000000000000000000000000..9a3b3ec627842583b96e7e7ef5eb7cd2af18cc98
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
@@ -0,0 +1,56 @@
+# 交互控制模块
+
+## 模块目标
+
+实现 DOM 启动保护、应用状态初始化和事件绑定，让新增、搜索、筛选、状态变更、删除等核心交互按设计数据流运行。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 归一化、持久化、筛选、渲染模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不实现 JSON 文件解析和 Blob 下载细节。
+- 不新增后端或异步服务。
+- 不弹出删除二次确认。
+
+## 任务 checklist
+
+- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
+- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
+- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
+- [ ] 绑定任务表单提交事件。
+- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
+- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
+- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
+- [ ] 新增成功后清理表单到可继续录入状态。
+- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
+- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
+- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
+- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
+- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
+- [ ] 删除任务时不弹二次确认。
+- [ ] 所有操作反馈写入统一反馈区域。
+
+## 验收标准
+
+- 模块在非浏览器环境加载不会失败。
+- 新增有效任务后任务出现在对应状态列，KPI 和存储同步更新。
+- 空标题提交不会新增任务。
+- 搜索和筛选改变可见任务，但不写入存储。
+- 卡片状态变更和删除能准确定位对应任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
+- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
+- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
+
+## 风险和注意事项
+
+- 事件绑定只应初始化一次，避免多次 render 后重复触发。
+- 任务状态更新后必须经过保存和重渲染，不能只改 DOM。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
new file mode 100644
index 0000000000000000000000000000000000000000..c8c471f1bfa250c2a130c18870b3c143eb8e9931
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
@@ -0,0 +1,59 @@
+# JSON 导入导出模块
+
+## 模块目标
+
+实现当前完整任务列表的 JSON 导出，以及任务数组或 `{ "tasks": [...] }` 对象格式的原子导入替换。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 归一化模块输出
+- 持久化模块输出
+- 渲染模块输出
+- 交互控制模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不合并导入任务和当前任务。
+- 不接受设计文档之外的导入格式。
+- 不在导入失败时覆盖当前任务数据。
+
+## 任务 checklist
+
+- [ ] 绑定 JSON 导出按钮事件。
+- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
+- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
+- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
+- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
+- [ ] 绑定 JSON 导入控件或文件输入事件。
+- [ ] 读取导入文件文本并执行 `JSON.parse`。
+- [ ] 接受任务数组格式：`[{...}, {...}]`。
+- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
+- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
+- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
+- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
+- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
+- [ ] 导入空数组时视为合法导入，替换为无任务状态。
+- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
+
+## 验收标准
+
+- 导出 JSON 表示完整任务列表。
+- 导入任务数组会替换当前任务列表。
+- 导入 `{ "tasks": [...] }` 会替换当前任务列表。
+- 非法 JSON、合法 JSON 但格式错误、`tasks` 非数组都不会覆盖当前数据。
+- 成功导入后 KPI、看板、负责人筛选和 `localStorage` 同步更新。
+
+## 测试要求
+
+- [ ] 人工验证导出文件内容包含完整任务列表。
+- [ ] 验证数组导入、对象导入、空数组导入。
+- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
+- [ ] 验证导入失败后现有任务仍保留。
+
+## 风险和注意事项
+
+- 导入替换必须是原子性的，不能边解析边覆盖当前状态。
+- 导出下载链接创建后应及时清理，避免 DOM 残留。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
new file mode 100644
index 0000000000000000000000000000000000000000..c477d58b4f86906322d8992ac0fb15bb72e561be
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
@@ -0,0 +1,48 @@
+# 指标计算模块
+
+## 模块目标
+
+实现 `calculateMetrics`，基于完整任务列表计算 KPI：总任务数、完成百分比、总工作量、未完成高优先级任务数。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读取筛选条件。
+- 不操作 DOM。
+- 不读写 `localStorage`。
+
+## 任务 checklist
+
+- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
+- [ ] 计算总任务数为完整任务数组长度。
+- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
+- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
+- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
+- [ ] 计算总工作量为所有任务 `effort` 求和。
+- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
+- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
+- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
+
+## 验收标准
+
+- 空任务列表返回总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`。
+- 全部任务完成时完成百分比为 `100%`。
+- 完成百分比按任务数量计算，不按工作量加权。
+- 筛选条件改变时 KPI 仍反映完整任务列表。
+
+## 测试要求
+
+- [ ] 验证空列表、部分完成、全部完成三种场景。
+- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
+- [ ] 验证工作量求和使用归一化后的数字。
+
+## 风险和注意事项
+
+- KPI 显示格式由渲染模块决定，计算模块应优先返回数值，避免字符串格式耦合。
+- 不要把筛选后的可见任务误传给 `calculateMetrics`。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
new file mode 100644
index 0000000000000000000000000000000000000000..549ae805a0ee8fd5425f6300cd192b965c387648
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
@@ -0,0 +1,49 @@
+# 数据归一化模块
+
+## 模块目标
+
+实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读写 DOM。
+- 不读写 `localStorage`。
+- 不决定任务是否保存或渲染。
+
+## 任务 checklist
+
+- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
+- [ ] 将 `title` 转为字符串并 trim。
+- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
+- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
+- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
+- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
+- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
+- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
+- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
+- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
+
+## 验收标准
+
+- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
+- 归一化函数不产生 DOM 或存储副作用。
+- 空标题任务不会被新增、导入或从存储中恢复到看板。
+- 无效状态、优先级和工作量不会破坏界面。
+
+## 测试要求
+
+- [ ] 补充或运行测试覆盖有效任务归一化。
+- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
+- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
+
+## 风险和注意事项
+
+- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
+- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
new file mode 100644
index 0000000000000000000000000000000000000000..b94aa88fa29ef4f691f0e06445950b9776216711
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
@@ -0,0 +1,49 @@
+# 页面结构模块
+
+## 模块目标
+
+实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 现有 `index.html`
+- 现有契约测试声明的必要元素 id、文本和 selector
+
+## 不做什么
+
+- 不实现业务逻辑、状态管理或数据持久化。
+- 不引入框架、CDN、外部字体、图片或构建工具。
+- 不创建营销 landing page。
+
+## 任务 checklist
+
+- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
+- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
+- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
+- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
+- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
+- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
+- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
+- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
+- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
+- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
+
+## 验收标准
+
+- 页面不是营销页，首屏包含实际工作看板。
+- 四个状态列都存在，并使用正确的 `data-status` 值。
+- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
+- 所有表单控件具备可访问 label。
+- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
+- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。
+
+## 风险和注意事项
+
+- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
+- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
new file mode 100644
index 0000000000000000000000000000000000000000..8e0fae9b4d5e54500e64efe9ed6f98d49e304c95
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
@@ -0,0 +1,50 @@
+# 持久化模块
+
+## 模块目标
+
+实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- 数据归一化模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不渲染 DOM。
+- 不处理筛选条件。
+- 不实现 JSON 文件导入导出。
+
+## 任务 checklist
+
+- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
+- [ ] 在保存前确保写入的是可序列化任务数组。
+- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
+- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
+- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
+- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
+- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
+- [ ] 对读取到的每条任务执行 `normalizeTask`。
+- [ ] 过滤空标题任务，避免无效任务进入应用状态。
+- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
+
+## 验收标准
+
+- 首次打开且无固定 key 时出现 sample tasks。
+- 固定 key 存在为空数组时，看板保持空任务状态。
+- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
+- 保存、新增、删除、状态变更和导入后使用同一个固定 key。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
+- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
+- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
+
+## 风险和注意事项
+
+- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
+- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
new file mode 100644
index 0000000000000000000000000000000000000000..f27641ce8a850b4b51d956870c59b07e95ebe05a
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
@@ -0,0 +1,56 @@
+# Sprint Board Lite 总体任务进度
+
+## 目标
+
+基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。
+
+## 模块进度
+
+- [ ] 页面结构模块：`doc/tasks/page-structure.md`
+- [ ] 数据模型模块：`doc/tasks/data-model.md`
+- [ ] 数据归一化模块：`doc/tasks/normalization.md`
+- [ ] 持久化模块：`doc/tasks/persistence.md`
+- [ ] 指标计算模块：`doc/tasks/metrics.md`
+- [ ] 筛选模块：`doc/tasks/filtering.md`
+- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
+- [ ] 交互控制模块：`doc/tasks/interactions.md`
+- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
+- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
+- [ ] 可访问性模块：`doc/tasks/accessibility.md`
+- [ ] 验证模块：`doc/tasks/verification.md`
+
+## 推荐执行顺序
+
+1. 页面结构模块
+2. 数据模型模块
+3. 数据归一化模块
+4. 持久化模块
+5. 指标计算模块
+6. 筛选模块
+7. 看板渲染模块
+8. 交互控制模块
+9. JSON 导入导出模块
+10. 样式和响应式模块
+11. 可访问性模块
+12. 验证模块
+
+## 可并行项
+
+- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
+- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
+- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
+- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
+
+## 阻塞项
+
+- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
+
+## 跨模块注意事项
+
+- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
+- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
+- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
+- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
+- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
+- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
+- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ca3e699d07ce48175fe50897f5ecc10978bedc5
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
@@ -0,0 +1,54 @@
+# 样式和响应式模块
+
+## 模块目标
+
+实现安静、密集、实用的 dashboard 工具界面，并保证桌面和移动端下 KPI、表单、筛选器、看板列和任务卡片可读可操作。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 看板渲染模块输出
+- `src/styles.css`
+
+## 不做什么
+
+- 不使用外部字体、图片、CDN、框架或装饰性渐变。
+- 不制作营销页视觉。
+- 不用 viewport width 直接缩放字体。
+
+## 任务 checklist
+
+- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
+- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
+- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
+- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
+- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
+- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
+- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
+- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
+- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
+- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
+- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
+
+## 验收标准
+
+- 桌面端页面密集、清晰、适合重复操作。
+- 移动端文本不重叠，表单和卡片可操作。
+- 看板列、卡片和控件尺寸稳定。
+- UI 不依赖外部资源。
+- 页面没有装饰性渐变、外部图片或 landing page 构图。
+
+## 测试要求
+
+- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
+- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
+- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
+- [ ] 验证键盘 focus 状态清晰可见。
+
+## 风险和注意事项
+
+- 颜色系统应服务状态识别，不要让页面变成单一色调。
+- 样式不能隐藏契约测试要求的文本或元素。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
new file mode 100644
index 0000000000000000000000000000000000000000..c0b96b74833e7c4c760885681c4bb8680b5c9c51
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
@@ -0,0 +1,57 @@
+# 验证模块
+
+## 模块目标
+
+在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 所有实现模块输出
+- `tests/test_static_contract.py`
+
+## 不做什么
+
+- 不跳过、删除、弱化或重写现有契约测试。
+- 不用补充测试替代契约测试。
+- 不引入自动化测试框架或构建工具。
+
+## 任务 checklist
+
+- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
+- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
+- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
+- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
+- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
+- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
+- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
+- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
+- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
+- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
+- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
+- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
+- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
+- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
+- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
+- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
+
+## 验收标准
+
+- 契约测试全部通过。
+- 需求文档列出的最终手动 smoke test 全部通过。
+- 设计文档列出的边界情况至少完成人工或自动验证。
+- 不存在业务代码之外的无关修改。
+
+## 测试要求
+
+- [ ] 必须执行 `python3 -m unittest discover -s tests`。
+- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
+- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
+
+## 风险和注意事项
+
+- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
+- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。

codex
`rg` 在这个环境里不可用，我会用 `grep` 做同样的 checklist 核对。`git status` 显示仓库上层已有未跟踪项，所以我会限定到 `doc/tasks` 路径确认本次改动范围。
exec
/bin/bash -lc "grep -R -n '"'^- '"\\[[ x]\\]' doc/tasks" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
doc/tasks/json-import-export.md:25:- [ ] 绑定 JSON 导出按钮事件。
doc/tasks/json-import-export.md:26:- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
doc/tasks/json-import-export.md:27:- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
doc/tasks/json-import-export.md:28:- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
doc/tasks/json-import-export.md:29:- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
doc/tasks/json-import-export.md:30:- [ ] 绑定 JSON 导入控件或文件输入事件。
doc/tasks/json-import-export.md:31:- [ ] 读取导入文件文本并执行 `JSON.parse`。
doc/tasks/json-import-export.md:32:- [ ] 接受任务数组格式：`[{...}, {...}]`。
doc/tasks/json-import-export.md:33:- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
doc/tasks/json-import-export.md:34:- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
doc/tasks/json-import-export.md:35:- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
doc/tasks/json-import-export.md:36:- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
doc/tasks/json-import-export.md:37:- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
doc/tasks/json-import-export.md:38:- [ ] 导入空数组时视为合法导入，替换为无任务状态。
doc/tasks/json-import-export.md:39:- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
doc/tasks/json-import-export.md:51:- [ ] 人工验证导出文件内容包含完整任务列表。
doc/tasks/json-import-export.md:52:- [ ] 验证数组导入、对象导入、空数组导入。
doc/tasks/json-import-export.md:53:- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
doc/tasks/json-import-export.md:54:- [ ] 验证导入失败后现有任务仍保留。
doc/tasks/accessibility.md:23:- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
doc/tasks/accessibility.md:24:- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
doc/tasks/accessibility.md:25:- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
doc/tasks/accessibility.md:26:- [ ] 为反馈区域添加 `aria-live="polite"`。
doc/tasks/accessibility.md:27:- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
doc/tasks/accessibility.md:28:- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
doc/tasks/accessibility.md:29:- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
doc/tasks/accessibility.md:30:- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
doc/tasks/accessibility.md:31:- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
doc/tasks/accessibility.md:32:- [ ] 检查移动端控件点击目标和文本可读性。
doc/tasks/accessibility.md:43:- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
doc/tasks/accessibility.md:44:- [ ] 人工检查 label 与控件 id 的关联。
doc/tasks/accessibility.md:45:- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
doc/tasks/accessibility.md:46:- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
doc/tasks/progress.md:9:- [ ] 页面结构模块：`doc/tasks/page-structure.md`
doc/tasks/progress.md:10:- [ ] 数据模型模块：`doc/tasks/data-model.md`
doc/tasks/progress.md:11:- [ ] 数据归一化模块：`doc/tasks/normalization.md`
doc/tasks/progress.md:12:- [ ] 持久化模块：`doc/tasks/persistence.md`
doc/tasks/progress.md:13:- [ ] 指标计算模块：`doc/tasks/metrics.md`
doc/tasks/progress.md:14:- [ ] 筛选模块：`doc/tasks/filtering.md`
doc/tasks/progress.md:15:- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
doc/tasks/progress.md:16:- [ ] 交互控制模块：`doc/tasks/interactions.md`
doc/tasks/progress.md:17:- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
doc/tasks/progress.md:18:- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
doc/tasks/progress.md:19:- [ ] 可访问性模块：`doc/tasks/accessibility.md`
doc/tasks/progress.md:20:- [ ] 验证模块：`doc/tasks/verification.md`
doc/tasks/progress.md:39:- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
doc/tasks/progress.md:40:- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
doc/tasks/progress.md:41:- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
doc/tasks/progress.md:42:- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
doc/tasks/progress.md:46:- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
doc/tasks/progress.md:50:- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
doc/tasks/progress.md:51:- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
doc/tasks/progress.md:52:- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
doc/tasks/progress.md:53:- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
doc/tasks/progress.md:54:- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
doc/tasks/progress.md:55:- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
doc/tasks/progress.md:56:- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
doc/tasks/interactions.md:23:- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
doc/tasks/interactions.md:24:- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
doc/tasks/interactions.md:25:- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
doc/tasks/interactions.md:26:- [ ] 绑定任务表单提交事件。
doc/tasks/interactions.md:27:- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
doc/tasks/interactions.md:28:- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
doc/tasks/interactions.md:29:- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
doc/tasks/interactions.md:30:- [ ] 新增成功后清理表单到可继续录入状态。
doc/tasks/interactions.md:31:- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
doc/tasks/interactions.md:32:- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
doc/tasks/interactions.md:33:- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
doc/tasks/interactions.md:34:- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
doc/tasks/interactions.md:35:- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
doc/tasks/interactions.md:36:- [ ] 删除任务时不弹二次确认。
doc/tasks/interactions.md:37:- [ ] 所有操作反馈写入统一反馈区域。
doc/tasks/interactions.md:49:- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
doc/tasks/interactions.md:50:- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
doc/tasks/interactions.md:51:- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
doc/tasks/normalization.md:22:- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
doc/tasks/normalization.md:23:- [ ] 将 `title` 转为字符串并 trim。
doc/tasks/normalization.md:24:- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
doc/tasks/normalization.md:25:- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
doc/tasks/normalization.md:26:- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
doc/tasks/normalization.md:27:- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
doc/tasks/normalization.md:28:- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
doc/tasks/normalization.md:29:- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
doc/tasks/normalization.md:30:- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
doc/tasks/normalization.md:31:- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
doc/tasks/normalization.md:42:- [ ] 补充或运行测试覆盖有效任务归一化。
doc/tasks/normalization.md:43:- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
doc/tasks/normalization.md:44:- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
doc/tasks/styles-responsive.md:23:- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
doc/tasks/styles-responsive.md:24:- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
doc/tasks/styles-responsive.md:25:- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
doc/tasks/styles-responsive.md:26:- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
doc/tasks/styles-responsive.md:27:- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
doc/tasks/styles-responsive.md:28:- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
doc/tasks/styles-responsive.md:29:- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
doc/tasks/styles-responsive.md:30:- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
doc/tasks/styles-responsive.md:31:- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
doc/tasks/styles-responsive.md:32:- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
doc/tasks/styles-responsive.md:33:- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
doc/tasks/styles-responsive.md:34:- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
doc/tasks/styles-responsive.md:46:- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
doc/tasks/styles-responsive.md:47:- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
doc/tasks/styles-responsive.md:48:- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
doc/tasks/styles-responsive.md:49:- [ ] 验证键盘 focus 状态清晰可见。
doc/tasks/persistence.md:23:- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
doc/tasks/persistence.md:24:- [ ] 在保存前确保写入的是可序列化任务数组。
doc/tasks/persistence.md:25:- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
doc/tasks/persistence.md:26:- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
doc/tasks/persistence.md:27:- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
doc/tasks/persistence.md:28:- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
doc/tasks/persistence.md:29:- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
doc/tasks/persistence.md:30:- [ ] 对读取到的每条任务执行 `normalizeTask`。
doc/tasks/persistence.md:31:- [ ] 过滤空标题任务，避免无效任务进入应用状态。
doc/tasks/persistence.md:32:- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
doc/tasks/persistence.md:43:- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
doc/tasks/persistence.md:44:- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
doc/tasks/persistence.md:45:- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
doc/tasks/verification.md:22:- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
doc/tasks/verification.md:23:- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
doc/tasks/verification.md:24:- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
doc/tasks/verification.md:25:- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
doc/tasks/verification.md:26:- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
doc/tasks/verification.md:27:- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
doc/tasks/verification.md:28:- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
doc/tasks/verification.md:29:- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
doc/tasks/verification.md:30:- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
doc/tasks/verification.md:31:- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
doc/tasks/verification.md:32:- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
doc/tasks/verification.md:33:- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
doc/tasks/verification.md:34:- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
doc/tasks/verification.md:35:- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
doc/tasks/verification.md:36:- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
doc/tasks/verification.md:37:- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
doc/tasks/verification.md:38:- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
doc/tasks/verification.md:39:- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
doc/tasks/verification.md:50:- [ ] 必须执行 `python3 -m unittest discover -s tests`。
doc/tasks/verification.md:51:- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
doc/tasks/verification.md:52:- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
doc/tasks/data-model.md:21:- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
doc/tasks/data-model.md:22:- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
doc/tasks/data-model.md:23:- [ ] 定义优先级集合：`low`、`medium`、`high`。
doc/tasks/data-model.md:24:- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
doc/tasks/data-model.md:25:- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
doc/tasks/data-model.md:26:- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
doc/tasks/data-model.md:27:- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
doc/tasks/data-model.md:28:- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
doc/tasks/data-model.md:29:- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
doc/tasks/data-model.md:30:- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
doc/tasks/data-model.md:41:- [ ] 使用契约测试确认固定存储 key 仍符合要求。
doc/tasks/data-model.md:42:- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
doc/tasks/metrics.md:22:- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
doc/tasks/metrics.md:23:- [ ] 计算总任务数为完整任务数组长度。
doc/tasks/metrics.md:24:- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
doc/tasks/metrics.md:25:- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
doc/tasks/metrics.md:26:- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
doc/tasks/metrics.md:27:- [ ] 计算总工作量为所有任务 `effort` 求和。
doc/tasks/metrics.md:28:- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
doc/tasks/metrics.md:29:- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
doc/tasks/metrics.md:30:- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
doc/tasks/metrics.md:41:- [ ] 验证空列表、部分完成、全部完成三种场景。
doc/tasks/metrics.md:42:- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
doc/tasks/metrics.md:43:- [ ] 验证工作量求和使用归一化后的数字。
doc/tasks/board-rendering.md:24:- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
doc/tasks/board-rendering.md:25:- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
doc/tasks/board-rendering.md:26:- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
doc/tasks/board-rendering.md:27:- [ ] 使用 `filterTasks` 计算可见任务。
doc/tasks/board-rendering.md:28:- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
doc/tasks/board-rendering.md:29:- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
doc/tasks/board-rendering.md:30:- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
doc/tasks/board-rendering.md:31:- [ ] 为每个任务卡片创建状态变更控件。
doc/tasks/board-rendering.md:32:- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
doc/tasks/board-rendering.md:33:- [ ] 为没有可见任务的列插入简洁 empty state。
doc/tasks/board-rendering.md:34:- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
doc/tasks/board-rendering.md:35:- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
doc/tasks/board-rendering.md:47:- [ ] 运行契约测试，确认 `renderBoard` 存在。
doc/tasks/board-rendering.md:48:- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
doc/tasks/board-rendering.md:49:- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
doc/tasks/filtering.md:22:- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
doc/tasks/filtering.md:23:- [ ] 支持 `query` 关键词搜索，大小写不敏感。
doc/tasks/filtering.md:24:- [ ] 让关键词至少匹配标题、负责人和备注。
doc/tasks/filtering.md:25:- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
doc/tasks/filtering.md:26:- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
doc/tasks/filtering.md:27:- [ ] 将搜索、状态和负责人筛选条件组合为交集。
doc/tasks/filtering.md:28:- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
doc/tasks/filtering.md:29:- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
doc/tasks/filtering.md:30:- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
doc/tasks/filtering.md:31:- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
doc/tasks/filtering.md:42:- [ ] 验证关键词匹配标题、负责人和备注。
doc/tasks/filtering.md:43:- [ ] 验证状态筛选、负责人筛选和组合筛选。
doc/tasks/filtering.md:44:- [ ] 验证大小写不敏感搜索。
doc/tasks/filtering.md:45:- [ ] 验证 owner 选项去重和 `All` 首项规则。
doc/tasks/page-structure.md:22:- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
doc/tasks/page-structure.md:23:- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
doc/tasks/page-structure.md:24:- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
doc/tasks/page-structure.md:25:- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
doc/tasks/page-structure.md:26:- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
doc/tasks/page-structure.md:27:- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
doc/tasks/page-structure.md:28:- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
doc/tasks/page-structure.md:29:- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
doc/tasks/page-structure.md:30:- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
doc/tasks/page-structure.md:31:- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
doc/tasks/page-structure.md:43:- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
doc/tasks/page-structure.md:44:- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。

exec
/bin/bash -lc "sed -n '1,120p' doc/tasks/progress.md" in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
# Sprint Board Lite 总体任务进度

## 目标

基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。

## 模块进度

- [ ] 页面结构模块：`doc/tasks/page-structure.md`
- [ ] 数据模型模块：`doc/tasks/data-model.md`
- [ ] 数据归一化模块：`doc/tasks/normalization.md`
- [ ] 持久化模块：`doc/tasks/persistence.md`
- [ ] 指标计算模块：`doc/tasks/metrics.md`
- [ ] 筛选模块：`doc/tasks/filtering.md`
- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
- [ ] 交互控制模块：`doc/tasks/interactions.md`
- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
- [ ] 可访问性模块：`doc/tasks/accessibility.md`
- [ ] 验证模块：`doc/tasks/verification.md`

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

- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。

## 阻塞项

- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。

## 跨模块注意事项

- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。

exec
/bin/bash -lc 'git rev-parse --show-toplevel' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
/Users/bytedance/Documents/Programs/Vibe2Spec

exec
/bin/bash -lc 'git status --short -- doc/tasks doc/proposal.md doc/detailed-design.md index.html src tests' in /Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
 succeeded in 0ms:
?? doc/detailed-design.md
?? doc/proposal.md
?? doc/tasks/
?? index.html
?? src/
?? tests/

diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
new file mode 100644
index 0000000000000000000000000000000000000000..4492ef8775d1c928654803af7436c0c471a67919
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
@@ -0,0 +1,51 @@
+# 可访问性模块
+
+## 模块目标
+
+保证 Sprint Board Lite 的表单、筛选器、任务卡片、状态变更、删除、导入导出和反馈区域具备基本键盘可用性和语义可理解性。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 交互控制模块输出
+- 样式和响应式模块输出
+
+## 不做什么
+
+- 不引入额外可访问性库。
+- 不改变已确认的产品规则。
+- 不用颜色作为唯一信息表达方式。
+
+## 任务 checklist
+
+- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
+- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
+- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
+- [ ] 为反馈区域添加 `aria-live="polite"`。
+- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
+- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
+- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
+- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
+- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
+- [ ] 检查移动端控件点击目标和文本可读性。
+
+## 验收标准
+
+- 所有高频交互可通过键盘完成。
+- 所有表单控件和筛选控件可被辅助技术理解。
+- 操作反馈不会只通过视觉位置变化表达。
+- 任务状态和优先级不只依赖颜色。
+
+## 测试要求
+
+- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
+- [ ] 人工检查 label 与控件 id 的关联。
+- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
+- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
+
+## 风险和注意事项
+
+- 动态创建卡片时容易遗漏控件 label 或可访问名称，应在渲染函数中统一生成。
+- focus 样式不能被全局 reset 或低对比度颜色覆盖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
new file mode 100644
index 0000000000000000000000000000000000000000..a533ed9f26d917675e91724bdb0a4d5a85624d5c
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
@@ -0,0 +1,54 @@
+# 看板渲染模块
+
+## 模块目标
+
+实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 指标计算模块输出
+- 筛选模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不绑定全局启动事件。
+- 不直接读取表单输入。
+- 不直接解析 JSON 文件。
+
+## 任务 checklist
+
+- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
+- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
+- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
+- [ ] 使用 `filterTasks` 计算可见任务。
+- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
+- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
+- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为每个任务卡片创建状态变更控件。
+- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
+- [ ] 为没有可见任务的列插入简洁 empty state。
+- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
+- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
+
+## 验收标准
+
+- 所有任务变更后重渲染不会产生重复卡片。
+- KPI 始终显示完整任务列表指标。
+- 空列显示 empty state。
+- 卡片包含需求文档列出的所有任务字段。
+- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `renderBoard` 存在。
+- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
+- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
+
+## 风险和注意事项
+
+- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
+- 重建 owner 选项时不要错误清空用户当前有效筛选值。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
new file mode 100644
index 0000000000000000000000000000000000000000..f164a168dc9e1382dae45a34fd84ac8119bdfb70
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
@@ -0,0 +1,47 @@
+# 数据模型模块
+
+## 模块目标
+
+定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- `src/app.js`
+
+## 不做什么
+
+- 不直接操作 DOM。
+- 不直接读写 `localStorage`。
+- 不实现筛选、指标计算或 JSON 导入导出。
+
+## 任务 checklist
+
+- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
+- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
+- [ ] 定义优先级集合：`low`、`medium`、`high`。
+- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
+- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
+- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
+- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
+- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
+- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
+- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
+
+## 验收标准
+
+- 数据结构与设计文档中的任务对象一致。
+- 状态、优先级和筛选默认值可被后续模块复用。
+- 存储 key 固定且只定义一处。
+- 模块加载时不会因为缺少浏览器 API 报错。
+
+## 测试要求
+
+- [ ] 使用契约测试确认固定存储 key 仍符合要求。
+- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
+
+## 风险和注意事项
+
+- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
+- 显示文案可以变化，但内部值不可随意变化。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
new file mode 100644
index 0000000000000000000000000000000000000000..386f69f51e872994f3adf1b145b70cbb9fa34c44
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
@@ -0,0 +1,50 @@
+# 筛选模块
+
+## 模块目标
+
+实现 `filterTasks` 和负责人筛选选项生成规则，让搜索、状态筛选和负责人筛选影响看板可见任务，同时不改变完整任务列表。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不计算 KPI。
+- 不读写 `localStorage`。
+- 不删除或修改任务数据。
+
+## 任务 checklist
+
+- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
+- [ ] 支持 `query` 关键词搜索，大小写不敏感。
+- [ ] 让关键词至少匹配标题、负责人和备注。
+- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
+- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
+- [ ] 将搜索、状态和负责人筛选条件组合为交集。
+- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
+- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
+- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
+- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
+
+## 验收标准
+
+- 搜索和筛选只影响可见任务，不改变 `appState.tasks`。
+- 筛选无结果时四个看板列仍然存在。
+- 负责人筛选选项不会从当前搜索结果派生，而是从完整任务列表派生。
+- 删除某负责人最后一个任务后，失效 owner 筛选会回退到 `All`。
+
+## 测试要求
+
+- [ ] 验证关键词匹配标题、负责人和备注。
+- [ ] 验证状态筛选、负责人筛选和组合筛选。
+- [ ] 验证大小写不敏感搜索。
+- [ ] 验证 owner 选项去重和 `All` 首项规则。
+
+## 风险和注意事项
+
+- `filterTasks` 应保持纯函数，不要在其中修改 filters。
+- owner 失效回退可以由渲染或交互模块处理，但必须在重渲染前生效。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
new file mode 100644
index 0000000000000000000000000000000000000000..9a3b3ec627842583b96e7e7ef5eb7cd2af18cc98
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
@@ -0,0 +1,56 @@
+# 交互控制模块
+
+## 模块目标
+
+实现 DOM 启动保护、应用状态初始化和事件绑定，让新增、搜索、筛选、状态变更、删除等核心交互按设计数据流运行。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 归一化、持久化、筛选、渲染模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不实现 JSON 文件解析和 Blob 下载细节。
+- 不新增后端或异步服务。
+- 不弹出删除二次确认。
+
+## 任务 checklist
+
+- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
+- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
+- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
+- [ ] 绑定任务表单提交事件。
+- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
+- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
+- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
+- [ ] 新增成功后清理表单到可继续录入状态。
+- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
+- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
+- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
+- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
+- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
+- [ ] 删除任务时不弹二次确认。
+- [ ] 所有操作反馈写入统一反馈区域。
+
+## 验收标准
+
+- 模块在非浏览器环境加载不会失败。
+- 新增有效任务后任务出现在对应状态列，KPI 和存储同步更新。
+- 空标题提交不会新增任务。
+- 搜索和筛选改变可见任务，但不写入存储。
+- 卡片状态变更和删除能准确定位对应任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
+- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
+- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
+
+## 风险和注意事项
+
+- 事件绑定只应初始化一次，避免多次 render 后重复触发。
+- 任务状态更新后必须经过保存和重渲染，不能只改 DOM。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
new file mode 100644
index 0000000000000000000000000000000000000000..c8c471f1bfa250c2a130c18870b3c143eb8e9931
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
@@ -0,0 +1,59 @@
+# JSON 导入导出模块
+
+## 模块目标
+
+实现当前完整任务列表的 JSON 导出，以及任务数组或 `{ "tasks": [...] }` 对象格式的原子导入替换。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 归一化模块输出
+- 持久化模块输出
+- 渲染模块输出
+- 交互控制模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不合并导入任务和当前任务。
+- 不接受设计文档之外的导入格式。
+- 不在导入失败时覆盖当前任务数据。
+
+## 任务 checklist
+
+- [ ] 绑定 JSON 导出按钮事件。
+- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
+- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
+- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
+- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
+- [ ] 绑定 JSON 导入控件或文件输入事件。
+- [ ] 读取导入文件文本并执行 `JSON.parse`。
+- [ ] 接受任务数组格式：`[{...}, {...}]`。
+- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
+- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
+- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
+- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
+- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
+- [ ] 导入空数组时视为合法导入，替换为无任务状态。
+- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
+
+## 验收标准
+
+- 导出 JSON 表示完整任务列表。
+- 导入任务数组会替换当前任务列表。
+- 导入 `{ "tasks": [...] }` 会替换当前任务列表。
+- 非法 JSON、合法 JSON 但格式错误、`tasks` 非数组都不会覆盖当前数据。
+- 成功导入后 KPI、看板、负责人筛选和 `localStorage` 同步更新。
+
+## 测试要求
+
+- [ ] 人工验证导出文件内容包含完整任务列表。
+- [ ] 验证数组导入、对象导入、空数组导入。
+- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
+- [ ] 验证导入失败后现有任务仍保留。
+
+## 风险和注意事项
+
+- 导入替换必须是原子性的，不能边解析边覆盖当前状态。
+- 导出下载链接创建后应及时清理，避免 DOM 残留。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
new file mode 100644
index 0000000000000000000000000000000000000000..c477d58b4f86906322d8992ac0fb15bb72e561be
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
@@ -0,0 +1,48 @@
+# 指标计算模块
+
+## 模块目标
+
+实现 `calculateMetrics`，基于完整任务列表计算 KPI：总任务数、完成百分比、总工作量、未完成高优先级任务数。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读取筛选条件。
+- 不操作 DOM。
+- 不读写 `localStorage`。
+
+## 任务 checklist
+
+- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
+- [ ] 计算总任务数为完整任务数组长度。
+- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
+- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
+- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
+- [ ] 计算总工作量为所有任务 `effort` 求和。
+- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
+- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
+- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
+
+## 验收标准
+
+- 空任务列表返回总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`。
+- 全部任务完成时完成百分比为 `100%`。
+- 完成百分比按任务数量计算，不按工作量加权。
+- 筛选条件改变时 KPI 仍反映完整任务列表。
+
+## 测试要求
+
+- [ ] 验证空列表、部分完成、全部完成三种场景。
+- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
+- [ ] 验证工作量求和使用归一化后的数字。
+
+## 风险和注意事项
+
+- KPI 显示格式由渲染模块决定，计算模块应优先返回数值，避免字符串格式耦合。
+- 不要把筛选后的可见任务误传给 `calculateMetrics`。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
new file mode 100644
index 0000000000000000000000000000000000000000..549ae805a0ee8fd5425f6300cd192b965c387648
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
@@ -0,0 +1,49 @@
+# 数据归一化模块
+
+## 模块目标
+
+实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读写 DOM。
+- 不读写 `localStorage`。
+- 不决定任务是否保存或渲染。
+
+## 任务 checklist
+
+- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
+- [ ] 将 `title` 转为字符串并 trim。
+- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
+- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
+- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
+- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
+- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
+- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
+- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
+- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
+
+## 验收标准
+
+- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
+- 归一化函数不产生 DOM 或存储副作用。
+- 空标题任务不会被新增、导入或从存储中恢复到看板。
+- 无效状态、优先级和工作量不会破坏界面。
+
+## 测试要求
+
+- [ ] 补充或运行测试覆盖有效任务归一化。
+- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
+- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
+
+## 风险和注意事项
+
+- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
+- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
new file mode 100644
index 0000000000000000000000000000000000000000..b94aa88fa29ef4f691f0e06445950b9776216711
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
@@ -0,0 +1,49 @@
+# 页面结构模块
+
+## 模块目标
+
+实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 现有 `index.html`
+- 现有契约测试声明的必要元素 id、文本和 selector
+
+## 不做什么
+
+- 不实现业务逻辑、状态管理或数据持久化。
+- 不引入框架、CDN、外部字体、图片或构建工具。
+- 不创建营销 landing page。
+
+## 任务 checklist
+
+- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
+- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
+- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
+- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
+- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
+- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
+- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
+- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
+- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
+- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
+
+## 验收标准
+
+- 页面不是营销页，首屏包含实际工作看板。
+- 四个状态列都存在，并使用正确的 `data-status` 值。
+- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
+- 所有表单控件具备可访问 label。
+- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
+- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。
+
+## 风险和注意事项
+
+- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
+- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
new file mode 100644
index 0000000000000000000000000000000000000000..8e0fae9b4d5e54500e64efe9ed6f98d49e304c95
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
@@ -0,0 +1,50 @@
+# 持久化模块
+
+## 模块目标
+
+实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- 数据归一化模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不渲染 DOM。
+- 不处理筛选条件。
+- 不实现 JSON 文件导入导出。
+
+## 任务 checklist
+
+- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
+- [ ] 在保存前确保写入的是可序列化任务数组。
+- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
+- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
+- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
+- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
+- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
+- [ ] 对读取到的每条任务执行 `normalizeTask`。
+- [ ] 过滤空标题任务，避免无效任务进入应用状态。
+- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
+
+## 验收标准
+
+- 首次打开且无固定 key 时出现 sample tasks。
+- 固定 key 存在为空数组时，看板保持空任务状态。
+- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
+- 保存、新增、删除、状态变更和导入后使用同一个固定 key。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
+- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
+- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
+
+## 风险和注意事项
+
+- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
+- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
new file mode 100644
index 0000000000000000000000000000000000000000..f27641ce8a850b4b51d956870c59b07e95ebe05a
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
@@ -0,0 +1,56 @@
+# Sprint Board Lite 总体任务进度
+
+## 目标
+
+基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。
+
+## 模块进度
+
+- [ ] 页面结构模块：`doc/tasks/page-structure.md`
+- [ ] 数据模型模块：`doc/tasks/data-model.md`
+- [ ] 数据归一化模块：`doc/tasks/normalization.md`
+- [ ] 持久化模块：`doc/tasks/persistence.md`
+- [ ] 指标计算模块：`doc/tasks/metrics.md`
+- [ ] 筛选模块：`doc/tasks/filtering.md`
+- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
+- [ ] 交互控制模块：`doc/tasks/interactions.md`
+- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
+- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
+- [ ] 可访问性模块：`doc/tasks/accessibility.md`
+- [ ] 验证模块：`doc/tasks/verification.md`
+
+## 推荐执行顺序
+
+1. 页面结构模块
+2. 数据模型模块
+3. 数据归一化模块
+4. 持久化模块
+5. 指标计算模块
+6. 筛选模块
+7. 看板渲染模块
+8. 交互控制模块
+9. JSON 导入导出模块
+10. 样式和响应式模块
+11. 可访问性模块
+12. 验证模块
+
+## 可并行项
+
+- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
+- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
+- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
+- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
+
+## 阻塞项
+
+- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
+
+## 跨模块注意事项
+
+- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
+- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
+- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
+- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
+- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
+- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
+- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ca3e699d07ce48175fe50897f5ecc10978bedc5
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
@@ -0,0 +1,54 @@
+# 样式和响应式模块
+
+## 模块目标
+
+实现安静、密集、实用的 dashboard 工具界面，并保证桌面和移动端下 KPI、表单、筛选器、看板列和任务卡片可读可操作。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 看板渲染模块输出
+- `src/styles.css`
+
+## 不做什么
+
+- 不使用外部字体、图片、CDN、框架或装饰性渐变。
+- 不制作营销页视觉。
+- 不用 viewport width 直接缩放字体。
+
+## 任务 checklist
+
+- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
+- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
+- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
+- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
+- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
+- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
+- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
+- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
+- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
+- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
+- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
+
+## 验收标准
+
+- 桌面端页面密集、清晰、适合重复操作。
+- 移动端文本不重叠，表单和卡片可操作。
+- 看板列、卡片和控件尺寸稳定。
+- UI 不依赖外部资源。
+- 页面没有装饰性渐变、外部图片或 landing page 构图。
+
+## 测试要求
+
+- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
+- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
+- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
+- [ ] 验证键盘 focus 状态清晰可见。
+
+## 风险和注意事项
+
+- 颜色系统应服务状态识别，不要让页面变成单一色调。
+- 样式不能隐藏契约测试要求的文本或元素。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
new file mode 100644
index 0000000000000000000000000000000000000000..c0b96b74833e7c4c760885681c4bb8680b5c9c51
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
@@ -0,0 +1,57 @@
+# 验证模块
+
+## 模块目标
+
+在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 所有实现模块输出
+- `tests/test_static_contract.py`
+
+## 不做什么
+
+- 不跳过、删除、弱化或重写现有契约测试。
+- 不用补充测试替代契约测试。
+- 不引入自动化测试框架或构建工具。
+
+## 任务 checklist
+
+- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
+- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
+- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
+- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
+- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
+- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
+- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
+- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
+- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
+- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
+- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
+- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
+- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
+- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
+- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
+- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
+
+## 验收标准
+
+- 契约测试全部通过。
+- 需求文档列出的最终手动 smoke test 全部通过。
+- 设计文档列出的边界情况至少完成人工或自动验证。
+- 不存在业务代码之外的无关修改。
+
+## 测试要求
+
+- [ ] 必须执行 `python3 -m unittest discover -s tests`。
+- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
+- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
+
+## 风险和注意事项
+
+- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
+- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。

codex
已完成任务阶段产物，未修改业务代码。

生成内容：
- 总体进度：[progress.md](/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md)
- 模块任务文件：`page-structure`、`data-model`、`normalization`、`persistence`、`metrics`、`filtering`、`board-rendering`、`interactions`、`json-import-export`、`styles-responsive`、`accessibility`
- 额外验证模块：`verification.md`，用于承接契约测试和手动 smoke test 约束

我已核对 `doc/tasks` 下共 13 个 Markdown 文件，均使用 checklist 表示任务状态。没有发现会阻塞任务划分的未明确点，因此未向你追加提问。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
new file mode 100644
index 0000000000000000000000000000000000000000..4492ef8775d1c928654803af7436c0c471a67919
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/accessibility.md
@@ -0,0 +1,51 @@
+# 可访问性模块
+
+## 模块目标
+
+保证 Sprint Board Lite 的表单、筛选器、任务卡片、状态变更、删除、导入导出和反馈区域具备基本键盘可用性和语义可理解性。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 交互控制模块输出
+- 样式和响应式模块输出
+
+## 不做什么
+
+- 不引入额外可访问性库。
+- 不改变已确认的产品规则。
+- 不用颜色作为唯一信息表达方式。
+
+## 任务 checklist
+
+- [ ] 检查所有表单控件都有显式 `label` 和正确 `for` 关联。
+- [ ] 检查搜索、状态筛选和负责人筛选具备可理解 label。
+- [ ] 检查导出按钮、导入控件、删除按钮和状态变更控件具备明确文本或上下文。
+- [ ] 为反馈区域添加 `aria-live="polite"`。
+- [ ] 确保空标题提交、导入成功和导入失败反馈会写入反馈区域。
+- [ ] 确保任务卡片展示优先级和状态文本，不只用颜色表达。
+- [ ] 确保键盘用户可以聚焦并操作表单、筛选器、状态控件、删除按钮和导入导出控件。
+- [ ] 确保 focus 状态在按钮、输入框、select 和文件输入上清晰可见。
+- [ ] 检查动态渲染任务卡片后，控件仍保持可访问名称。
+- [ ] 检查移动端控件点击目标和文本可读性。
+
+## 验收标准
+
+- 所有高频交互可通过键盘完成。
+- 所有表单控件和筛选控件可被辅助技术理解。
+- 操作反馈不会只通过视觉位置变化表达。
+- 任务状态和优先级不只依赖颜色。
+
+## 测试要求
+
+- [ ] 使用键盘完成新增、搜索、筛选、状态变更、删除、导出和选择导入文件。
+- [ ] 人工检查 label 与控件 id 的关联。
+- [ ] 人工检查反馈区域在表单错误和导入错误时更新。
+- [ ] 运行契约测试，确认可访问性调整未破坏必要结构。
+
+## 风险和注意事项
+
+- 动态创建卡片时容易遗漏控件 label 或可访问名称，应在渲染函数中统一生成。
+- focus 样式不能被全局 reset 或低对比度颜色覆盖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
new file mode 100644
index 0000000000000000000000000000000000000000..a533ed9f26d917675e91724bdb0a4d5a85624d5c
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/board-rendering.md
@@ -0,0 +1,54 @@
+# 看板渲染模块
+
+## 模块目标
+
+实现 `renderBoard`，将完整任务列表和当前筛选条件渲染为 KPI、负责人筛选选项、四列看板、任务卡片和 empty state。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 指标计算模块输出
+- 筛选模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不绑定全局启动事件。
+- 不直接读取表单输入。
+- 不直接解析 JSON 文件。
+
+## 任务 checklist
+
+- [ ] 实现 `renderBoard(tasks, filters)` named function，并保护缺少 DOM 时的调用。
+- [ ] 在渲染开始时使用 `calculateMetrics` 计算完整任务列表 KPI。
+- [ ] 更新总任务数、完成百分比、总工作量和未完成高优先级任务数的 DOM 文本。
+- [ ] 使用 `filterTasks` 计算可见任务。
+- [ ] 将可见任务按 `backlog`、`doing`、`review`、`done` 分组。
+- [ ] 每次渲染前清空四列任务容器，避免重复卡片。
+- [ ] 为每个任务创建卡片，展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为每个任务卡片创建状态变更控件。
+- [ ] 为每个任务卡片创建删除控件，并携带可定位任务 id。
+- [ ] 为没有可见任务的列插入简洁 empty state。
+- [ ] 重新生成负责人筛选选项，并保留或回退当前 owner 筛选值。
+- [ ] 避免在渲染中重复绑定每张卡片的独立事件监听，优先配合事件委托。
+
+## 验收标准
+
+- 所有任务变更后重渲染不会产生重复卡片。
+- KPI 始终显示完整任务列表指标。
+- 空列显示 empty state。
+- 卡片包含需求文档列出的所有任务字段。
+- 卡片状态控件和删除控件包含任务 id，后续交互可准确定位任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `renderBoard` 存在。
+- [ ] 人工验证空任务、筛选无结果、单列多任务和四列都有任务的渲染状态。
+- [ ] 验证新增、删除、状态变更和导入后的 DOM 不重复、不残留旧卡片。
+
+## 风险和注意事项
+
+- `renderBoard` 需要容错处理缺失 DOM 节点，避免测试环境直接调用时报错。
+- 重建 owner 选项时不要错误清空用户当前有效筛选值。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
new file mode 100644
index 0000000000000000000000000000000000000000..f164a168dc9e1382dae45a34fd84ac8119bdfb70
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/data-model.md
@@ -0,0 +1,47 @@
+# 数据模型模块
+
+## 模块目标
+
+定义任务对象、状态常量、优先级常量、存储 key 和应用内存状态，为归一化、持久化、筛选和渲染提供统一数据结构。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- `src/app.js`
+
+## 不做什么
+
+- 不直接操作 DOM。
+- 不直接读写 `localStorage`。
+- 不实现筛选、指标计算或 JSON 导入导出。
+
+## 任务 checklist
+
+- [ ] 定义固定存储 key：`sprint-board-lite.tasks.v1`。
+- [ ] 定义状态集合：`backlog`、`doing`、`review`、`done`。
+- [ ] 定义优先级集合：`low`、`medium`、`high`。
+- [ ] 定义状态显示文案映射，用于卡片、列标题和状态控件展示。
+- [ ] 定义优先级显示文案映射，用于卡片和表单展示。
+- [ ] 定义内部任务对象字段：`id`、`title`、`owner`、`effort`、`priority`、`status`、`notes`。
+- [ ] 定义默认值规则：空负责人为 `Unassigned`，无效工作量为 `0`，无效优先级为 `medium`，无效状态为 `backlog`，缺失备注为空字符串。
+- [ ] 定义 `appState` 结构，包含 `tasks` 和 `filters`。
+- [ ] 将初始筛选状态设置为搜索空字符串、状态 `All`、负责人 `All`。
+- [ ] 确保常量和状态定义不会在非浏览器环境中访问 `window` 或 `document`。
+
+## 验收标准
+
+- 数据结构与设计文档中的任务对象一致。
+- 状态、优先级和筛选默认值可被后续模块复用。
+- 存储 key 固定且只定义一处。
+- 模块加载时不会因为缺少浏览器 API 报错。
+
+## 测试要求
+
+- [ ] 使用契约测试确认固定存储 key 仍符合要求。
+- [ ] 在非浏览器测试环境加载 `src/app.js`，确认不会立即访问 DOM 或 `localStorage`。
+
+## 风险和注意事项
+
+- 状态值和优先级值必须使用英文小写枚举，避免与契约测试或筛选逻辑不一致。
+- 显示文案可以变化，但内部值不可随意变化。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
new file mode 100644
index 0000000000000000000000000000000000000000..386f69f51e872994f3adf1b145b70cbb9fa34c44
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/filtering.md
@@ -0,0 +1,50 @@
+# 筛选模块
+
+## 模块目标
+
+实现 `filterTasks` 和负责人筛选选项生成规则，让搜索、状态筛选和负责人筛选影响看板可见任务，同时不改变完整任务列表。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不计算 KPI。
+- 不读写 `localStorage`。
+- 不删除或修改任务数据。
+
+## 任务 checklist
+
+- [ ] 实现 `filterTasks(tasks, filters)` named function，并确保可在非浏览器环境调用。
+- [ ] 支持 `query` 关键词搜索，大小写不敏感。
+- [ ] 让关键词至少匹配标题、负责人和备注。
+- [ ] 支持状态筛选；`All` 返回所有状态，其他值只返回对应状态。
+- [ ] 支持负责人筛选；`All` 返回所有负责人，其他值只返回对应负责人。
+- [ ] 将搜索、状态和负责人筛选条件组合为交集。
+- [ ] 实现负责人选项生成逻辑，来源为当前完整任务列表。
+- [ ] 确保负责人选项第一个值固定为 `All`，其余值去重。
+- [ ] 在新增、删除、导入任务后触发负责人选项重新生成。
+- [ ] 当前筛选 owner 已不存在时，将 owner 筛选回退为 `All`。
+
+## 验收标准
+
+- 搜索和筛选只影响可见任务，不改变 `appState.tasks`。
+- 筛选无结果时四个看板列仍然存在。
+- 负责人筛选选项不会从当前搜索结果派生，而是从完整任务列表派生。
+- 删除某负责人最后一个任务后，失效 owner 筛选会回退到 `All`。
+
+## 测试要求
+
+- [ ] 验证关键词匹配标题、负责人和备注。
+- [ ] 验证状态筛选、负责人筛选和组合筛选。
+- [ ] 验证大小写不敏感搜索。
+- [ ] 验证 owner 选项去重和 `All` 首项规则。
+
+## 风险和注意事项
+
+- `filterTasks` 应保持纯函数，不要在其中修改 filters。
+- owner 失效回退可以由渲染或交互模块处理，但必须在重渲染前生效。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
new file mode 100644
index 0000000000000000000000000000000000000000..9a3b3ec627842583b96e7e7ef5eb7cd2af18cc98
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/interactions.md
@@ -0,0 +1,56 @@
+# 交互控制模块
+
+## 模块目标
+
+实现 DOM 启动保护、应用状态初始化和事件绑定，让新增、搜索、筛选、状态变更、删除等核心交互按设计数据流运行。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 归一化、持久化、筛选、渲染模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不实现 JSON 文件解析和 Blob 下载细节。
+- 不新增后端或异步服务。
+- 不弹出删除二次确认。
+
+## 任务 checklist
+
+- [ ] 使用 `typeof document !== "undefined"` 保护 DOM 启动逻辑。
+- [ ] 在 DOM 可用后执行初始化，调用 `loadTasks()` 填充 `appState.tasks`。
+- [ ] 初始化 `appState.filters` 为 `query: ""`、`status: "All"`、`owner: "All"`。
+- [ ] 绑定任务表单提交事件。
+- [ ] 在表单提交时读取标题、负责人、工作量、优先级、状态和备注。
+- [ ] 标题为空或纯空白时显示简洁反馈，不新增任务。
+- [ ] 有效提交时调用 `normalizeTask`，追加到 `appState.tasks`，调用 `saveTasks`，再调用 `renderBoard`。
+- [ ] 新增成功后清理表单到可继续录入状态。
+- [ ] 绑定搜索输入事件，更新 `filters.query` 并重渲染，不写入 `localStorage`。
+- [ ] 绑定状态筛选事件，更新 `filters.status` 并重渲染。
+- [ ] 绑定负责人筛选事件，更新 `filters.owner` 并重渲染。
+- [ ] 使用事件委托处理卡片状态变更，按任务 id 更新 status、保存并重渲染。
+- [ ] 使用事件委托处理删除按钮，按任务 id 删除任务、保存并重渲染。
+- [ ] 删除任务时不弹二次确认。
+- [ ] 所有操作反馈写入统一反馈区域。
+
+## 验收标准
+
+- 模块在非浏览器环境加载不会失败。
+- 新增有效任务后任务出现在对应状态列，KPI 和存储同步更新。
+- 空标题提交不会新增任务。
+- 搜索和筛选改变可见任务，但不写入存储。
+- 卡片状态变更和删除能准确定位对应任务。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 DOM 启动保护和 named functions 不冲突。
+- [ ] 人工 smoke test：添加任务、移动任务、删除任务、搜索任务、按状态筛选、按负责人筛选。
+- [ ] 验证每次任务变更后刷新页面仍能恢复数据。
+
+## 风险和注意事项
+
+- 事件绑定只应初始化一次，避免多次 render 后重复触发。
+- 任务状态更新后必须经过保存和重渲染，不能只改 DOM。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
new file mode 100644
index 0000000000000000000000000000000000000000..c8c471f1bfa250c2a130c18870b3c143eb8e9931
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/json-import-export.md
@@ -0,0 +1,59 @@
+# JSON 导入导出模块
+
+## 模块目标
+
+实现当前完整任务列表的 JSON 导出，以及任务数组或 `{ "tasks": [...] }` 对象格式的原子导入替换。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 归一化模块输出
+- 持久化模块输出
+- 渲染模块输出
+- 交互控制模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不合并导入任务和当前任务。
+- 不接受设计文档之外的导入格式。
+- 不在导入失败时覆盖当前任务数据。
+
+## 任务 checklist
+
+- [ ] 绑定 JSON 导出按钮事件。
+- [ ] 导出完整 `appState.tasks`，不导出当前筛选后的可见任务。
+- [ ] 使用 `JSON.stringify(tasks, null, 2)` 生成可读 JSON。
+- [ ] 使用 Blob 和临时下载链接触发本地 JSON 文件下载。
+- [ ] 导出后不改变当前任务状态、筛选条件或存储内容。
+- [ ] 绑定 JSON 导入控件或文件输入事件。
+- [ ] 读取导入文件文本并执行 `JSON.parse`。
+- [ ] 接受任务数组格式：`[{...}, {...}]`。
+- [ ] 接受包含 `tasks` 数组的对象格式：`{"tasks": [{...}, {...}]}`。
+- [ ] 对其他格式显示简洁错误反馈，并保持当前任务列表不变。
+- [ ] 对每条导入任务执行 `normalizeTask`，并过滤空标题任务。
+- [ ] 仅在解析、格式识别和归一化完成后替换 `appState.tasks`。
+- [ ] 导入成功后调用 `saveTasks`，重置失效负责人筛选，调用 `renderBoard`。
+- [ ] 导入空数组时视为合法导入，替换为无任务状态。
+- [ ] 导入失败后清理文件输入值，允许用户重新选择同一文件。
+
+## 验收标准
+
+- 导出 JSON 表示完整任务列表。
+- 导入任务数组会替换当前任务列表。
+- 导入 `{ "tasks": [...] }` 会替换当前任务列表。
+- 非法 JSON、合法 JSON 但格式错误、`tasks` 非数组都不会覆盖当前数据。
+- 成功导入后 KPI、看板、负责人筛选和 `localStorage` 同步更新。
+
+## 测试要求
+
+- [ ] 人工验证导出文件内容包含完整任务列表。
+- [ ] 验证数组导入、对象导入、空数组导入。
+- [ ] 验证非法 JSON、无 `tasks` 数组对象和 `tasks` 非数组对象。
+- [ ] 验证导入失败后现有任务仍保留。
+
+## 风险和注意事项
+
+- 导入替换必须是原子性的，不能边解析边覆盖当前状态。
+- 导出下载链接创建后应及时清理，避免 DOM 残留。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
new file mode 100644
index 0000000000000000000000000000000000000000..c477d58b4f86906322d8992ac0fb15bb72e561be
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/metrics.md
@@ -0,0 +1,48 @@
+# 指标计算模块
+
+## 模块目标
+
+实现 `calculateMetrics`，基于完整任务列表计算 KPI：总任务数、完成百分比、总工作量、未完成高优先级任务数。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读取筛选条件。
+- 不操作 DOM。
+- 不读写 `localStorage`。
+
+## 任务 checklist
+
+- [ ] 实现 `calculateMetrics(tasks)` named function，并确保可在非浏览器环境调用。
+- [ ] 计算总任务数为完整任务数组长度。
+- [ ] 计算完成百分比为 `done` 状态任务数量除以总任务数。
+- [ ] 当总任务数为 `0` 时，将完成百分比设为 `0`。
+- [ ] 将完成百分比四舍五入为整数百分比显示所需值。
+- [ ] 计算总工作量为所有任务 `effort` 求和。
+- [ ] 计算未完成高优先级任务数为 `priority === "high"` 且 `status !== "done"` 的任务数量。
+- [ ] 返回结构化 metrics 对象，供 `renderBoard` 更新 KPI 区。
+- [ ] 确保计算结果不受搜索、状态筛选或负责人筛选影响。
+
+## 验收标准
+
+- 空任务列表返回总数 `0`、完成 `0%`、工作量 `0`、未完成高优先级 `0`。
+- 全部任务完成时完成百分比为 `100%`。
+- 完成百分比按任务数量计算，不按工作量加权。
+- 筛选条件改变时 KPI 仍反映完整任务列表。
+
+## 测试要求
+
+- [ ] 验证空列表、部分完成、全部完成三种场景。
+- [ ] 验证高优先级 done 任务不计入未完成高优先级数量。
+- [ ] 验证工作量求和使用归一化后的数字。
+
+## 风险和注意事项
+
+- KPI 显示格式由渲染模块决定，计算模块应优先返回数值，避免字符串格式耦合。
+- 不要把筛选后的可见任务误传给 `calculateMetrics`。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
new file mode 100644
index 0000000000000000000000000000000000000000..549ae805a0ee8fd5425f6300cd192b965c387648
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/normalization.md
@@ -0,0 +1,49 @@
+# 数据归一化模块
+
+## 模块目标
+
+实现 `normalizeTask`，作为表单输入、sample tasks、localStorage 数据和 JSON 导入数据进入内部状态前的统一入口。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不读写 DOM。
+- 不读写 `localStorage`。
+- 不决定任务是否保存或渲染。
+
+## 任务 checklist
+
+- [ ] 实现 `normalizeTask(input)` named function，并确保可被测试直接发现或调用。
+- [ ] 将 `title` 转为字符串并 trim。
+- [ ] 将 `owner` 转为字符串并 trim，空值归一化为 `Unassigned`。
+- [ ] 将 `notes` 转为字符串并 trim，缺失时归一化为空字符串。
+- [ ] 将 `effort` 解析为有限、非负数字；空值、负数、`NaN` 和无限值归一化为 `0`。
+- [ ] 校验 `priority` 是否为 `low`、`medium`、`high`，否则归一化为 `medium`。
+- [ ] 校验 `status` 是否为 `backlog`、`doing`、`review`、`done`，否则归一化为 `backlog`。
+- [ ] 保留已有 `id` 的字符串值；缺失或空值时生成稳定字符串 id。
+- [ ] 在调用方过滤空标题任务，保证空标题记录不进入看板。
+- [ ] 将 `normalizeTask` 挂载到浏览器可访问位置，同时保护非浏览器环境。
+
+## 验收标准
+
+- 任意输入对象都能得到标准任务对象，或被调用方作为无效空标题过滤。
+- 归一化函数不产生 DOM 或存储副作用。
+- 空标题任务不会被新增、导入或从存储中恢复到看板。
+- 无效状态、优先级和工作量不会破坏界面。
+
+## 测试要求
+
+- [ ] 补充或运行测试覆盖有效任务归一化。
+- [ ] 验证空标题、空负责人、负工作量、非数字工作量、非法优先级和非法状态。
+- [ ] 验证缺失 id 时生成字符串 id，已有 id 时保留。
+
+## 风险和注意事项
+
+- `normalizeTask` 不应自己丢弃空标题，否则调用方难以区分无效输入和归一化结果；调用方应显式过滤。
+- id 生成只需要浏览器端稳定可用，不应引入外部依赖。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
new file mode 100644
index 0000000000000000000000000000000000000000..b94aa88fa29ef4f691f0e06445950b9776216711
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/page-structure.md
@@ -0,0 +1,49 @@
+# 页面结构模块
+
+## 模块目标
+
+实现 Sprint Board Lite 的静态 HTML 骨架，让首屏直接呈现可操作的冲刺看板、任务表单、筛选器、KPI 区和导入导出控件。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 现有 `index.html`
+- 现有契约测试声明的必要元素 id、文本和 selector
+
+## 不做什么
+
+- 不实现业务逻辑、状态管理或数据持久化。
+- 不引入框架、CDN、外部字体、图片或构建工具。
+- 不创建营销 landing page。
+
+## 任务 checklist
+
+- [ ] 梳理契约测试要求的页面标题、主标题、元素 id、基础文案和 selector，并记录到实现笔记中。
+- [ ] 实现 concise header，确保页面标题、主标题或 header 中包含 `Sprint Board Lite`。
+- [ ] 实现 KPI 指标区，预留总任务数、完成百分比、总工作量、未完成高优先级任务数的静态容器。
+- [ ] 实现任务录入表单，包含标题、负责人、工作量、优先级、状态和备注字段。
+- [ ] 为每个表单控件补充显式 `label`，并用 `for` 关联对应控件 id。
+- [ ] 实现搜索输入、状态筛选、负责人筛选、JSON 导出按钮、JSON 导入控件和文件输入。
+- [ ] 实现四个看板列：Backlog、Doing、Review、Done，并为每列添加对应 `data-status`。
+- [ ] 为每个看板列预留任务列表容器，供 `renderBoard` 填充任务卡片和 empty state。
+- [ ] 添加简洁反馈区域，并配置为后续导入、表单校验和操作反馈使用。
+- [ ] 检查首屏信息密度，确保打开页面后直接看到工作看板和任务操作区。
+
+## 验收标准
+
+- 页面不是营销页，首屏包含实际工作看板。
+- 四个状态列都存在，并使用正确的 `data-status` 值。
+- 表单字段、筛选控件、导入导出控件和 KPI 容器完整存在。
+- 所有表单控件具备可访问 label。
+- 静态 HTML 不依赖 JavaScript 才能生成主要页面骨架。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认必要元素 id、文本和 selector 未丢失。
+- [ ] 人工打开页面，确认首屏能看到 header、KPI、表单、筛选器和四列看板。
+
+## 风险和注意事项
+
+- 契约测试可能依赖具体 id 或文案，修改 HTML 前必须先对照测试要求。
+- 页面骨架应为 JavaScript 渲染留出稳定挂载点，避免后续模块反复调整结构。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
new file mode 100644
index 0000000000000000000000000000000000000000..8e0fae9b4d5e54500e64efe9ed6f98d49e304c95
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/persistence.md
@@ -0,0 +1,50 @@
+# 持久化模块
+
+## 模块目标
+
+实现 `saveTasks` 和 `loadTasks`，使用固定 `localStorage` key 持久化任务，并在无存储或损坏存储场景下保持页面可恢复。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 数据模型模块输出
+- 数据归一化模块输出
+- `src/app.js`
+
+## 不做什么
+
+- 不渲染 DOM。
+- 不处理筛选条件。
+- 不实现 JSON 文件导入导出。
+
+## 任务 checklist
+
+- [ ] 实现 `saveTasks(tasks)` named function，并使用固定 key `sprint-board-lite.tasks.v1` 写入 JSON。
+- [ ] 在保存前确保写入的是可序列化任务数组。
+- [ ] 捕获 `localStorage` 不可用或写入失败的异常，避免应用崩溃。
+- [ ] 实现 `loadTasks()` named function，并保护非浏览器环境。
+- [ ] 当固定 key 不存在时，加载少量有用 sample tasks。
+- [ ] 仅在固定 key 不存在时 seed sample tasks；key 存在但为空数组、损坏或无有效任务时不得再次 seed。
+- [ ] 解析存储 JSON，并只接受数组格式作为持久化任务列表。
+- [ ] 对读取到的每条任务执行 `normalizeTask`。
+- [ ] 过滤空标题任务，避免无效任务进入应用状态。
+- [ ] 对损坏 JSON 或格式错误返回可恢复结果，不阻塞首次渲染。
+
+## 验收标准
+
+- 首次打开且无固定 key 时出现 sample tasks。
+- 固定 key 存在为空数组时，看板保持空任务状态。
+- 固定 key 存在但 JSON 损坏时，页面不崩溃且不重新 seed sample tasks。
+- 保存、新增、删除、状态变更和导入后使用同一个固定 key。
+
+## 测试要求
+
+- [ ] 运行契约测试，确认 `saveTasks` 和 `loadTasks` 存在。
+- [ ] 模拟无 `localStorage` 环境，确认函数不会抛出未捕获异常。
+- [ ] 模拟 key 缺失、空数组、损坏 JSON 和包含无效任务的存储数据。
+
+## 风险和注意事项
+
+- sample tasks 的 seed 条件必须区分 key 缺失和 key 存在但内容异常。
+- `loadTasks` 不应在模块加载时自动执行，避免非浏览器测试环境失败。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
new file mode 100644
index 0000000000000000000000000000000000000000..f27641ce8a850b4b51d956870c59b07e95ebe05a
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/progress.md
@@ -0,0 +1,56 @@
+# Sprint Board Lite 总体任务进度
+
+## 目标
+
+基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将 Sprint Board Lite 拆分为可逐步执行、可验证的最小任务。实现阶段只应修改 `index.html`、`src/styles.css`、`src/app.js`，必要时补充 focused tests；不得引入后端、构建工具、框架、远程资源或第三方依赖。
+
+## 模块进度
+
+- [ ] 页面结构模块：`doc/tasks/page-structure.md`
+- [ ] 数据模型模块：`doc/tasks/data-model.md`
+- [ ] 数据归一化模块：`doc/tasks/normalization.md`
+- [ ] 持久化模块：`doc/tasks/persistence.md`
+- [ ] 指标计算模块：`doc/tasks/metrics.md`
+- [ ] 筛选模块：`doc/tasks/filtering.md`
+- [ ] 看板渲染模块：`doc/tasks/board-rendering.md`
+- [ ] 交互控制模块：`doc/tasks/interactions.md`
+- [ ] JSON 导入导出模块：`doc/tasks/json-import-export.md`
+- [ ] 样式和响应式模块：`doc/tasks/styles-responsive.md`
+- [ ] 可访问性模块：`doc/tasks/accessibility.md`
+- [ ] 验证模块：`doc/tasks/verification.md`
+
+## 推荐执行顺序
+
+1. 页面结构模块
+2. 数据模型模块
+3. 数据归一化模块
+4. 持久化模块
+5. 指标计算模块
+6. 筛选模块
+7. 看板渲染模块
+8. 交互控制模块
+9. JSON 导入导出模块
+10. 样式和响应式模块
+11. 可访问性模块
+12. 验证模块
+
+## 可并行项
+
+- [ ] 数据模型、归一化、指标计算可以在页面结构完成基本容器后并行推进。
+- [ ] 样式和响应式可以在页面结构确定后与 JavaScript 逻辑并行推进。
+- [ ] 可访问性可以与页面结构、交互控制和样式模块同步检查。
+- [ ] JSON 导出导入可以在持久化和归一化模块完成后独立实现。
+
+## 阻塞项
+
+- [ ] 当前无已知阻塞。实现阶段如发现契约测试与设计文档存在冲突，应先停下并确认。
+
+## 跨模块注意事项
+
+- [ ] 所有外部输入必须经过 `normalizeTask` 后进入内部状态。
+- [ ] 所有任务变更必须经过内存状态更新、`saveTasks` 和 `renderBoard`。
+- [ ] KPI 计算始终基于完整任务列表，不受搜索或筛选条件影响。
+- [ ] JSON 导入必须原子替换完整任务列表，不做合并。
+- [ ] 负责人筛选选项必须来自当前完整任务列表，并包含 `All`。
+- [ ] DOM 启动逻辑必须保护非浏览器环境，避免契约测试加载模块时报错。
+- [ ] 最终验证必须运行 `python3 -m unittest discover -s tests`，并完成需求文档列出的手动 smoke test。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ca3e699d07ce48175fe50897f5ecc10978bedc5
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/styles-responsive.md
@@ -0,0 +1,54 @@
+# 样式和响应式模块
+
+## 模块目标
+
+实现安静、密集、实用的 dashboard 工具界面，并保证桌面和移动端下 KPI、表单、筛选器、看板列和任务卡片可读可操作。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 页面结构模块输出
+- 看板渲染模块输出
+- `src/styles.css`
+
+## 不做什么
+
+- 不使用外部字体、图片、CDN、框架或装饰性渐变。
+- 不制作营销页视觉。
+- 不用 viewport width 直接缩放字体。
+
+## 任务 checklist
+
+- [ ] 定义基础颜色、边框、间距和字体系统，以中性色为主体并使用有限状态色。
+- [ ] 实现 header、主区域、KPI、表单、工具区和看板的整体布局。
+- [ ] 在桌面端使用紧凑 dashboard 布局，避免过大的 hero 式排版。
+- [ ] 将 KPI 区设计为稳定网格，避免动态数值导致布局跳动。
+- [ ] 将任务表单和筛选工具区设计为易扫描、易操作的工作区。
+- [ ] 将四列看板设计为稳定网格，每列具备最小高度和明确边界。
+- [ ] 设计任务卡片样式，清晰展示标题、负责人、工作量、优先级、状态和备注。
+- [ ] 为不同优先级和状态提供文本可读的视觉区分，不只依赖颜色。
+- [ ] 为按钮、输入框、select、文件输入和卡片控件添加可见 focus 状态。
+- [ ] 实现移动端断点，使 KPI、表单、筛选器和看板列纵向堆叠。
+- [ ] 检查窄屏下长标题、长负责人、长备注和按钮文字不会重叠或溢出。
+- [ ] 确保 hover、focus 和动态内容不会改变固定格式控件的尺寸。
+
+## 验收标准
+
+- 桌面端页面密集、清晰、适合重复操作。
+- 移动端文本不重叠，表单和卡片可操作。
+- 看板列、卡片和控件尺寸稳定。
+- UI 不依赖外部资源。
+- 页面没有装饰性渐变、外部图片或 landing page 构图。
+
+## 测试要求
+
+- [ ] 人工检查桌面视口下 KPI、表单、筛选器和四列看板。
+- [ ] 人工检查移动视口下字段、按钮、卡片和列标题不重叠。
+- [ ] 使用长标题、长负责人和长备注任务验证换行和溢出处理。
+- [ ] 验证键盘 focus 状态清晰可见。
+
+## 风险和注意事项
+
+- 颜色系统应服务状态识别，不要让页面变成单一色调。
+- 样式不能隐藏契约测试要求的文本或元素。
diff --git a/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
new file mode 100644
index 0000000000000000000000000000000000000000..c0b96b74833e7c4c760885681c4bb8680b5c9c51
--- /dev/null
+++ b/experiments/web-harness-vs-direct-20260603/harness-flow/doc/tasks/verification.md
@@ -0,0 +1,57 @@
+# 验证模块
+
+## 模块目标
+
+在实现完成后验证契约测试、核心用户流程、边界情况、响应式布局和本地持久化行为，确保交付符合需求与设计文档。
+
+## 依赖输入
+
+- `doc/proposal.md`
+- `doc/detailed-design.md`
+- 所有实现模块输出
+- `tests/test_static_contract.py`
+
+## 不做什么
+
+- 不跳过、删除、弱化或重写现有契约测试。
+- 不用补充测试替代契约测试。
+- 不引入自动化测试框架或构建工具。
+
+## 任务 checklist
+
+- [ ] 运行 `python3 -m unittest discover -s tests`，记录结果。
+- [ ] 如契约测试失败，定位失败原因并只修复实现代码或必要文档任务，不修改契约测试。
+- [ ] 人工 smoke test：打开页面确认首屏是可操作看板。
+- [ ] 人工 smoke test：新增有效任务并确认对应列出现卡片。
+- [ ] 人工 smoke test：提交空标题任务并确认不会新增。
+- [ ] 人工 smoke test：移动任务到另一个状态并确认 KPI、看板和存储同步更新。
+- [ ] 人工 smoke test：删除任务并确认不需要二次确认。
+- [ ] 人工 smoke test：使用搜索、状态筛选和负责人筛选定位任务。
+- [ ] 人工 smoke test：确认筛选无结果时四列显示 empty state。
+- [ ] 人工 smoke test：导出 JSON 并确认文件代表完整任务列表。
+- [ ] 人工 smoke test：导入任务数组并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入 `{ "tasks": [...] }` 对象并确认替换当前任务列表。
+- [ ] 人工 smoke test：导入非法 JSON 并确认现有任务不变。
+- [ ] 验证刷新页面后任务从 `localStorage` 恢复。
+- [ ] 验证固定 key 为 `sprint-board-lite.tasks.v1`。
+- [ ] 验证 localStorage key 缺失时 seed sample tasks，key 存在为空数组或损坏时不重新 seed。
+- [ ] 验证移动端视口下文本不重叠，表单、筛选器和卡片可操作。
+- [ ] 验证所有表单控件有 label，交互控件有可见 focus 状态。
+
+## 验收标准
+
+- 契约测试全部通过。
+- 需求文档列出的最终手动 smoke test 全部通过。
+- 设计文档列出的边界情况至少完成人工或自动验证。
+- 不存在业务代码之外的无关修改。
+
+## 测试要求
+
+- [ ] 必须执行 `python3 -m unittest discover -s tests`。
+- [ ] 必须执行新增、状态变更、筛选、指标更新和导出 JSON 的手动 smoke test。
+- [ ] 建议补充 focused tests 覆盖纯函数边界，但不得替代现有契约测试。
+
+## 风险和注意事项
+
+- 当前项目是 dependency-free 静态应用，验证不能依赖 npm 或构建工具。
+- 手动验证失败时应回到对应模块修复，而不是放宽验收标准。

tokens used
60,626
