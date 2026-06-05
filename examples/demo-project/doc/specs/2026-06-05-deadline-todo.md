# deadline-todo

> Status: Implemented
> Owner: Demo
> Created: 2026-06-05
> Related: ../proposal.md

## Context

The demo needs a small but concrete feature that shows why Spec-first development reduces missed edge cases.

## Goals & Non-Goals

Goals:

- Store Todo title, due date, completed state, and id.
- Mark incomplete tasks overdue when the due date is earlier than today.

Non-Goals:

- Notifications.
- Backend sync.
- Authentication.

## User Stories

- As a user, I want overdue tasks to stand out, so that I can prioritize them.

## Functional Requirements (EARS)

- WHEN today's date is later than an incomplete Todo due date THE SYSTEM SHALL show an overdue label.
- WHEN a Todo is completed THE SYSTEM SHALL not show it as overdue.

## Data Model

```text
Todo {
  id: string
  title: string
  dueDate: string | ""
  completed: boolean
}
```

## Key Design Decisions (ADR)

### ADR-1: Compare date-only strings

Decision: Use local `YYYY-MM-DD` strings for due date comparison.

Why: The browser date input already emits this format, and lexical comparison avoids timestamp timezone drift for this MVP.

Alternatives: Convert to `Date`, but full timestamps can create off-by-one behavior around local midnight.

## Acceptance Criteria

GIVEN an incomplete Todo due yesterday
WHEN the app renders
THEN it shows an overdue label.

GIVEN an overdue Todo
WHEN the user completes it
THEN the overdue label disappears.

## Out of Scope

- Time-of-day reminders.
- Recurring tasks.

## References

- ../proposal.md
- ../detailed-design.md
- ../tasks/deadline-todo.md
