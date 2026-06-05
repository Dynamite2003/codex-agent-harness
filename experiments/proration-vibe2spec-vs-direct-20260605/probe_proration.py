from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Case:
    name: str
    current: float
    next: float
    start: str
    end: str
    change: str
    coupon: float
    tax: float
    expected_total: float | None
    expected_kind: str | None
    expected_period_days: int | None
    expected_affected_days: int | None


CASES = [
    Case("february 2026 coupon tax", 100, 160, "2026-02-01", "2026-03-01", "2026-02-15", 10, 8.25, 29.23, "charge", 28, 14),
    Case("leap year february", 100, 160, "2024-02-01", "2024-03-01", "2024-02-15", 0, 0, 31.03, "charge", 29, 15),
    Case("downgrade refund", 160, 100, "2026-01-01", "2026-02-01", "2026-01-16", 0, 0, -30.97, "refund", 31, 16),
    Case("invalid end before start", 100, 160, "2026-03-01", "2026-02-01", "2026-02-15", 0, 0, None, None, None, None),
]


def main() -> int:
    target = Path(sys.argv[1]).resolve()
    text = target.read_text(encoding="utf-8")
    uses_fixed_30 = bool(re.search(r"periodDays\s*[:=]\s*30|/\s*30\b", text))
    exposes_function = "window.calculateProration" in text and "function calculateProration" in text
    actuals = [_simulate(text, case) for case in CASES]
    checks = [
        {"name": "exposes calculateProration", "ok": exposes_function},
        {"name": "does not use fixed 30-day billing period", "ok": not uses_fixed_30},
        *actuals,
    ]
    result = {
        "target": str(target),
        "passed": sum(1 for check in checks if check["ok"]),
        "total": len(checks),
        "checks": checks,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] == result["total"] else 1


def _simulate(text: str, case: Case) -> dict[str, object]:
    if re.search(r"periodDays\s*[:=]\s*30|/\s*30\b", text):
        period_days = 30
    else:
        period_days = _day_diff(case.start, case.end)
    affected_days = _day_diff(case.change, case.end)
    change_offset = _day_diff(case.start, case.change)

    if period_days <= 0 or change_offset < 0 or affected_days <= 0:
        actual = {"error": "Invalid date range"}
    else:
        delta = (case.next - case.current) * (affected_days / period_days)
        discounted = delta * (1 - case.coupon / 100)
        taxed = discounted * (1 + case.tax / 100)
        total = round(taxed + 1e-12, 2)
        actual = {
            "total": total,
            "kind": "charge" if total >= 0 else "refund",
            "periodDays": period_days,
            "affectedDays": affected_days,
        }

    if case.expected_total is None:
        ok = "error" in actual
    else:
        ok = (
            actual.get("total") == case.expected_total
            and actual.get("kind") == case.expected_kind
            and actual.get("periodDays") == case.expected_period_days
            and actual.get("affectedDays") == case.expected_affected_days
        )
    return {"name": case.name, "ok": ok, "actual": actual}


def _day_diff(start: str, end: str) -> int:
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


if __name__ == "__main__":
    raise SystemExit(main())
