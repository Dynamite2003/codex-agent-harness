# deadline-todo Tasks

## Module Goal

Implement a static Todo app with optional due dates, overdue labels, completion, deletion, and localStorage persistence.

## Dependencies

- `doc/proposal.md`
- `doc/detailed-design.md`
- `doc/specs/2026-06-05-deadline-todo.md`

## Out of Scope

- Backend API.
- Push reminders.
- Authentication.

## Checklist

- [x] Implement static HTML structure.
- [x] Implement Todo state load/save with localStorage.
- [x] Implement add, complete, and delete interactions.
- [x] Implement overdue calculation and visual label.
- [x] Verify empty-title validation and refresh persistence.

## Traceability

- EARS: `WHEN today's date is later than an incomplete Todo due date THE SYSTEM SHALL display the Todo as overdue.`
- ADR: one-file static implementation and date-only comparison.
- Acceptance: overdue label, complete removes overdue, refresh restores tasks.

## Test Requirements

- Manual browser smoke test.
- Source review for `isOverdue`.
- Refresh persistence verification.

## AFK/HITL

AFK: all tasks can be completed without user input.

HITL: none.

## Blocked by

None.

## Likely File Scope

- `index.html`
- `doc/verification.md`

## Risks

- localStorage may be blocked in some contexts; app should still render and show an error instead of crashing.
