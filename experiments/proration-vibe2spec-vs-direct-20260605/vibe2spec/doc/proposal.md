# Proration Calculator Proposal

## Context

Subscription proration is easy to implement incorrectly when requirements are only described as "按天计费". The important behavior is not the UI itself, but exact billing math across real billing-period length, leap years, coupons, tax, rounding, and refunds.

## Goals & Non-Goals

Goals:

- Calculate a prorated upgrade charge or downgrade refund for one billing period.
- Use actual billing-period day count.
- Apply coupon before tax.
- Apply tax to the net prorated delta.
- Round only the final result to cents.
- Reject invalid date ranges.

Non-Goals:

- No backend.
- No payment processing.
- No multi-currency support.
- No time-of-day proration.

## User Stories

- As a billing operator, I want exact proration, so that customer invoices match policy.
- As a support agent, I want downgrade refunds to show as negative amounts, so that I can explain credits.
- As a reviewer, I want invalid date ranges rejected, so that bad billing inputs do not create misleading numbers.

## Functional Requirements (EARS)

- WHEN billing end is not after billing start THE SYSTEM SHALL reject the input.
- WHEN change date is before billing start THE SYSTEM SHALL reject the input.
- WHEN change date is on or after billing end THE SYSTEM SHALL reject the input.
- WHEN inputs are valid THE SYSTEM SHALL calculate period days as the actual day difference between billing start and billing end.
- WHEN inputs are valid THE SYSTEM SHALL calculate affected days as the day difference from change date to billing end.
- WHEN inputs are valid THE SYSTEM SHALL calculate prorated delta as `(newPrice - currentPrice) * affectedDays / periodDays`.
- WHEN coupon percent is provided THE SYSTEM SHALL apply the coupon discount to the prorated delta before tax.
- WHEN tax percent is provided THE SYSTEM SHALL apply tax to the discounted prorated delta.
- WHEN the final amount is positive THE SYSTEM SHALL label it as a charge.
- WHEN the final amount is negative THE SYSTEM SHALL label it as a refund.
- WHEN displaying money THE SYSTEM SHALL round only the final amount to cents.

## Key Decisions / ADR Candidates

### ADR Candidate 1: Date-only UTC parsing

Decision: Parse `YYYY-MM-DD` inputs as UTC date-only values.

Why: JavaScript local `Date` parsing can introduce timezone drift. UTC date-only arithmetic gives stable day counts.

Alternatives: Local `Date`, but that risks daylight-saving and timezone differences.

### ADR Candidate 2: Final-only rounding

Decision: Keep intermediate math unrounded and round final amount to cents.

Why: Intermediate rounding accumulates billing errors.

Alternatives: Round daily rate first, but it can produce incorrect totals.

## Acceptance Criteria (GIVEN-WHEN-THEN)

GIVEN current price 100, new price 160, billing period 2026-02-01 to 2026-03-01, change date 2026-02-15, coupon 10%, and tax 8.25%
WHEN the calculator runs
THEN the charge is 29.23 because 2026 February has 28 days and 14 affected days.

GIVEN current price 100, new price 160, billing period 2024-02-01 to 2024-03-01, change date 2024-02-15, coupon 0%, and tax 0%
WHEN the calculator runs
THEN the charge is 31.03 because leap-year February has 29 days and 15 affected days.

GIVEN current price 160, new price 100, billing period 2026-01-01 to 2026-02-01, change date 2026-01-16, coupon 0%, and tax 0%
WHEN the calculator runs
THEN the result is a 30.97 refund.

GIVEN billing end is before billing start
WHEN the calculator runs
THEN it rejects the input.

## Out of Scope

- Payment collection.
- Invoice PDF generation.
- Multi-plan history.

## Constraints

- Static HTML only.
- No dependencies.
- Expose `window.calculateProration` for deterministic probing.

## Risks

- Date math can be off by one. Mitigation: use UTC date-only day difference.
- Rounding can hide errors. Mitigation: final-only rounding and fixture tests.

## Open Questions

- None for demo MVP.
