目标：
用户的具体需求是：# Experiment Task: Sprint Board Lite

Build a small dependency-free static web app named **Sprint Board Lite**.

The project already has a minimal static web scaffold and a Python unittest contract test suite. Implement the app until the tests pass, and add any focused tests or documentation you think are useful.

Do not delete, skip, weaken, or rewrite the existing contract tests to make the task easier. You may add complementary tests if they improve coverage.

## Product Goal

Sprint Board Lite helps a small team plan and track a sprint in the browser without a backend. The first screen should be the actual working board, not a landing page.

## Functional Requirements

- Use only plain HTML, CSS, and JavaScript. Do not add npm, build tooling, remote CDNs, external fonts, or framework dependencies.
- Implement these files:
  - `index.html`
  - `src/styles.css`
  - `src/app.js`
- The app must include:
  - A concise header with the product name.
  - KPI metrics for total tasks, completion percentage, total effort, and open high-priority tasks.
  - A task form with fields for title, owner, effort, priority, status, and notes.
  - A search input.
  - Status and owner filters.
  - Four board columns: Backlog, Doing, Review, Done.
  - Task cards that show title, owner, effort, priority, status, notes, and simple controls to change status or delete the task.
  - Empty states for columns with no visible tasks.
  - JSON export and import controls.
- Persist tasks in `localStorage` under the key `sprint-board-lite.tasks.v1`.
- Seed a few useful sample tasks only when localStorage is empty.
- Keep all UI text concise and suitable for a work tool.

## JavaScript Requirements

- `src/app.js` must expose named functions that can be inspected and reused:
  - `normalizeTask`
  - `calculateMetrics`
  - `filterTasks`
  - `saveTasks`
  - `loadTasks`
  - `renderBoard`
- Guard DOM startup so the module can be inspected without immediately failing in non-browser contexts.
- Validate task titles so blank titles are not added.
- Normalize effort to a finite non-negative number.
- Normalize status to one of `backlog`, `doing`, `review`, or `done`.
- Normalize priority to one of `low`, `medium`, or `high`.

## Design Requirements

- Make the app responsive for desktop and mobile widths.
- Use a dense, practical dashboard layout rather than a marketing page.
- Avoid external images and decorative gradients.
- Include accessible labels for form controls.
- Include visible focus states.
- Avoid text overlap and make cards readable on narrow screens.

## Verification

- Run `python3 -m unittest discover -s tests`.
- Open the page locally and do a manual smoke test:
  - Add a task.
  - Move it to another status.
  - Use search or filters.
  - Confirm metrics update.
  - Confirm export produces JSON.
现在只完成需求阶段，目标是生成清晰、可确认、可进入设计阶段的需求文档。

输入：
当前项目目录：/Users/bytedance/Documents/Programs/Vibe2Spec/experiments/web-harness-vs-direct-20260603/harness-flow
全局约束：
- 如果目标项目以 Python 为主要语言，进入 harness 前必须先通过 codex-harness bootstrap-python 准备 uv 隔离环境，并配置 ruff、mypy、pytest。
- 只执行当前阶段，不要提前进入后续阶段。
- 每个阶段都视为新的独立对话；不要依赖其他阶段的聊天历史，只能通过明确声明的文档 artifact 传递上下文。
- 不要揣测用户意图；任何关键不明确点必须向用户提问。
- 如果当前阶段需要用户回答才能继续，不要进入下一阶段所需的实质输出；最终回复必须包含独占一行的 HARNESS_NEEDS_USER_INPUT，并在其后列出需要用户回答的问题。harness 检测到该标记后会停止，不会继续后续阶段。
- 只修改当前阶段输出要求中声明的文件。
- 不要回滚用户已有改动。
上游 artifact：
- 无上游 artifact
Prompt 风格：语言：zh-CN；语气：direct；必须覆盖这些内容或标题：目标、输入、输出、步骤。
对话隔离：这是 需求 阶段的新对话，不要依赖其他阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

输出：
请在 doc/proposal.md 生成需求文档。
文档必须包含：背景、目标、非目标、用户故事或使用场景、功能需求、约束、待确认问题。

步骤：
先阅读项目目录和必要文件，判断需求是否依赖现有系统。
使用提问的方式确认不明确的需求；不要替用户补全关键决策。
如果信息足够，生成 proposal.md；如果信息不足，proposal.md 中必须列出阻塞问题和推荐的下一轮提问。
不要做设计、任务拆分或代码实现。
