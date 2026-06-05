from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


CSV_ROW_NUMBER_KEY = "__csv_row_number__"
UNCATEGORIZED = "Uncategorized"
MONEY_QUANT = Decimal("0.01")


def summarize_expenses(
    rows: Iterable[Mapping[str, Any]],
    min_amount: object = 0.0,
    currency: str = "USD",
) -> dict[str, object]:
    threshold = _parse_threshold(min_amount)
    categories: dict[str, Decimal] = {}
    grand_total = Decimal("0")
    count = 0

    for index, row in enumerate(rows, start=1):
        row_number = row.get(CSV_ROW_NUMBER_KEY, index)
        amount = _parse_amount(row, row_number)

        if amount < threshold:
            continue

        category = _normalize_category(row.get("category", ""))
        categories[category] = categories.get(category, Decimal("0")) + amount
        grand_total += amount
        count += 1

    return {
        "currency": str(currency).strip().upper(),
        "count": count,
        "grand_total": _as_money_number(grand_total),
        "categories": {
            category: _as_money_number(total) for category, total in categories.items()
        },
    }


def _parse_threshold(value: object) -> Decimal:
    try:
        threshold = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"invalid min_amount: {value!r}") from None

    if not threshold.is_finite():
        raise ValueError(f"invalid min_amount: {value!r}")

    return threshold


def _parse_amount(row: Mapping[str, Any], row_number: object) -> Decimal:
    if "amount" not in row or row["amount"] is None:
        raise ValueError(f"row {row_number} has missing amount")

    raw_amount = row["amount"]
    try:
        amount = Decimal(str(raw_amount).strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"row {row_number} has invalid amount: {raw_amount!r}") from None

    if not amount.is_finite():
        raise ValueError(f"row {row_number} has invalid amount: {raw_amount!r}")

    return amount


def _normalize_category(value: object) -> str:
    category = "" if value is None else str(value).strip()
    return category or UNCATEGORIZED


def _as_money_number(value: Decimal) -> float:
    return float(value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP))
