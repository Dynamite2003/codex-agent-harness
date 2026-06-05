# Proration Calculator Detailed Design

## Context and Design Scope

Implement a static proration calculator whose correctness is defined by the Spec fixtures in `doc/proposal.md`.

## Goals & Non-Goals

Goals:

- Deterministic date-only calculation.
- Final-only rounding.
- Clear charge/refund labeling.
- Invalid input rejection.

Non-Goals:

- Backend storage.
- Payment capture.
- Multi-currency support.

## Module Responsibilities

### Input UI

Collect prices, dates, coupon percent, and tax percent.

### Calculation Core

Expose `calculateProration(input)` for probes. Return either `{ error }` or `{ total, kind, periodDays, affectedDays }`.

### Rendering

Show charge/refund label, amount, and day-count explanation.

## API / Local Contracts

```text
calculateProration(input: {
  current: number
  next: number
  start: string
  end: string
  change: string
  coupon: number
  tax: number
}) -> { total, kind, periodDays, affectedDays } | { error }
```

## Key Design Decisions (ADR)

### ADR-1: UTC Date-Only Arithmetic

Decision: Parse date strings with `Date.UTC(year, month - 1, day)`.

Why: Day count must be independent of local timezone and daylight saving.

Alternatives / Tradeoffs: Native `new Date("YYYY-MM-DD")` is shorter but easier to misinterpret.

### ADR-2: Keep Negative Totals

Decision: Return negative totals for refunds and use `kind` for display.

Why: Keeping sign makes tests and downstream accounting clearer.

Alternatives / Tradeoffs: Return absolute amount and type only, but that loses useful numeric meaning.

## Acceptance Criteria Mapping

- February 2026 fixture: validates actual 28-day period, coupon-before-tax, final rounding.
- Leap-year fixture: validates 29-day February.
- Downgrade fixture: validates negative refund.
- Invalid range fixture: validates input rejection.

## Test Strategy

- Static probe calls `calculateProration` with billing fixtures.
- Render screenshot verifies no blank page.
- Artifact validator checks Spec-first docs.

## Spec Backfill Notes

No deviation recorded.
