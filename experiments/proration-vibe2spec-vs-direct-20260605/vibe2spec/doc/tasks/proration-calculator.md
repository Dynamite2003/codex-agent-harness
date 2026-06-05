# proration-calculator Tasks

## Module Goal

Implement a static subscription proration calculator with exact billing-period math.

## Dependencies

- `doc/proposal.md`
- `doc/detailed-design.md`

## Out of Scope

- Payments.
- Backend persistence.

## Checklist

- [x] Implement UTC date-only parsing.
- [x] Implement actual day-count calculation.
- [x] Implement coupon-before-tax calculation.
- [x] Implement final-only rounding.
- [x] Implement refund labeling for negative totals.
- [x] Implement invalid range rejection.
- [x] Expose `window.calculateProration`.

## Traceability

- EARS: actual period days, affected days, coupon before tax, tax after coupon, final-only rounding.
- ADR: UTC date-only arithmetic and signed refund totals.
- Acceptance: 2026 February, 2024 leap year, downgrade refund, invalid range rejection.

## Test Requirements

- Run `probe_proration.py` against implementation.
- Generate Chrome render screenshot.

## AFK/HITL

AFK.

## Blocked by

None.

## Likely File Scope

- `index.html`
- `doc/verification.md`
