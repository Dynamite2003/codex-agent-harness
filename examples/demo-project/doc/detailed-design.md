# Todo Deadline Detailed Design

## Context and Design Scope

This design implements the Todo deadline MVP in a single static HTML file. It preserves the Spec-first behavior from `doc/proposal.md` while staying dependency-free.

## Goals & Non-Goals

Goals:

- Render a usable Todo form and list.
- Persist Todo items in `localStorage`.
- Compute overdue state from due date and completed state.

Non-Goals:

- Backend API.
- Build tooling.
- Push reminders.

## Module Responsibilities

### UI Module

Responsible for rendering the form, validation message, Todo list, empty state, and action buttons.

### State Module

Responsible for loading, saving, adding, completing, and deleting Todo items.

### Date Module

Responsible for determining whether a Todo is overdue.

## API / Local Contracts

```text
addTodo(title: string, dueDate: string): void
toggleTodo(id: string): void
deleteTodo(id: string): void
isOverdue(todo: Todo, today: string): boolean
```

## Key Design Decisions (ADR)

### ADR-1: One-file static implementation

Decision: Keep HTML, CSS, and JavaScript in `index.html`.

Why: The demo must be inspectable and runnable without setup.

Alternatives / Tradeoffs: A component framework would scale better, but it would distract from the workflow demonstration.

### ADR-2: Store date-only strings

Decision: Store due dates as `YYYY-MM-DD`.

Why: Date input produces this value and lexical comparison is enough for date-only overdue logic.

Alternatives / Tradeoffs: JavaScript `Date` objects introduce timezone edge cases.

## Acceptance Criteria Mapping

- Add valid task: handled by `addTodo` and form submit.
- Empty title validation: handled before `addTodo`.
- Overdue label: handled by `isOverdue`.
- Complete overdue task: handled by `toggleTodo` and rerender.
- Refresh persistence: handled by `loadTodos` and `saveTodos`.

## Test Strategy

- Manual browser smoke test by opening `index.html`.
- Source-level review of `isOverdue` for completed tasks and empty due dates.
- Refresh test to verify `localStorage` persistence.

## Spec Backfill Notes

The final implementation matches the proposal and `doc/specs/2026-06-05-deadline-todo.md`; no behavior deviation is recorded.
