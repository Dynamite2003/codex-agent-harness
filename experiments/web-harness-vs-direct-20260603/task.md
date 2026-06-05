# Experiment Task: Sprint Board Lite

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
