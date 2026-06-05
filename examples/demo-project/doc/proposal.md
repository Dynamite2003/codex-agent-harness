# Todo Deadline MVP Proposal

## Context

当前 demo 是一个无依赖静态 Todo Web App。直接让 Codex 实现时，容易遗漏截止日期为空、逾期计算边界、localStorage 持久化和非目标范围。这里先把需求写成可实现、可验收的 Spec。

## Goals & Non-Goals

Goals:

- 支持新增、完成、删除 Todo。
- 支持可选截止日期。
- 未完成且截止日期早于今天的 Todo 显示为逾期。
- Todo 数据持久化到浏览器 `localStorage`。

Non-Goals:

- 不做账号、登录或云同步。
- 不做通知推送、邮件或日历集成。
- 不做复杂标签、优先级或多列表。

## User Stories

- As a user, I want to set a due date for a task, so that I can see which tasks are late.
- As a user, I want completed tasks to stop showing as overdue, so that the list reflects actual risk.
- As a user, I want tasks to persist after refresh, so that I do not lose my list.

## Functional Requirements (EARS)

- WHEN the user submits a non-empty task title THE SYSTEM SHALL create a Todo item.
- WHEN the user submits an empty task title THE SYSTEM SHALL keep the list unchanged and show inline validation.
- WHEN the user provides a due date THE SYSTEM SHALL store the due date as `YYYY-MM-DD`.
- WHEN today's date is later than an incomplete Todo due date THE SYSTEM SHALL display the Todo as overdue.
- WHEN a Todo is marked complete THE SYSTEM SHALL persist the completed state and remove overdue styling.
- WHEN a Todo is deleted THE SYSTEM SHALL remove it from localStorage.

## Key Decisions / ADR Candidates

### ADR Candidate 1: Keep the demo as static HTML

Decision: Implement the MVP in one `index.html` file with inline CSS and JavaScript.

Why: The course demo should run without dependency installation and remain easy to inspect.

Alternatives: Use React/Vite, but that adds setup cost unrelated to the workflow demonstration.

### ADR Candidate 2: Use localStorage

Decision: Persist Todo items in `localStorage`.

Why: It demonstrates persistence without a backend, accounts, or external services.

Alternatives: In-memory state only, but refresh would lose data and weaken the acceptance criteria.

## Acceptance Criteria (GIVEN-WHEN-THEN)

- GIVEN an empty list WHEN the user adds "Submit report" with tomorrow's date THEN the list shows one pending Todo with that due date.
- GIVEN a Todo due yesterday and incomplete WHEN the page renders THEN the Todo displays an overdue label.
- GIVEN an overdue Todo WHEN the user marks it complete THEN the overdue label is no longer shown.
- GIVEN a Todo list WHEN the user refreshes the page THEN the same Todo items are restored from localStorage.
- GIVEN an empty title WHEN the user submits the form THEN no Todo is added and validation text appears.

## Out of Scope

- Server storage.
- Push reminders.
- Multi-user collaboration.
- Date-time timezone customization.

## Constraints

- No build step.
- No external dependencies.
- Must work by opening `index.html` directly.

## Risks

- Date comparison can be off by timezone if using full timestamps. Mitigation: compare `YYYY-MM-DD` date-only strings.
- Browser localStorage may be unavailable in restricted contexts. Mitigation: keep the UI functional and fail gracefully.

## Open Questions

- None for MVP.
