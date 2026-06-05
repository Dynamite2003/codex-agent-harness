# Verification

## Manual Smoke Test

Status: Passed.

Steps:

1. Opened `index.html` directly in a browser.
2. Added a Todo with tomorrow's date.
3. Added a Todo with yesterday's date.
4. Confirmed the yesterday Todo shows `Overdue`.
5. Marked the overdue Todo complete.
6. Confirmed the overdue label disappears.
7. Refreshed the page.
8. Confirmed Todo items persisted.

## Source-Level Checks

- `isOverdue` returns `false` for completed Todos.
- `isOverdue` returns `false` when `dueDate` is empty.
- Due dates are stored and compared as `YYYY-MM-DD`.

## Spec Backfill

No deviation from `doc/proposal.md` or `doc/specs/2026-06-05-deadline-todo.md`.
