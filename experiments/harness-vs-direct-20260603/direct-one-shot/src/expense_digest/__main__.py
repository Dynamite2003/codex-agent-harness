from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from expense_digest.core import CSV_ROW_NUMBER_KEY, summarize_expenses


REQUIRED_COLUMNS = {"date", "category", "amount", "description"}


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m expense_digest")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--min-amount", default="0.0", metavar="FLOAT")
    parser.add_argument("--currency", default="USD", metavar="CODE")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        rows = _read_csv(args.csv_file)
        summary = summarize_expenses(
            rows,
            min_amount=args.min_amount,
            currency=args.currency,
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json.dump(summary, sys.stdout, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


def _read_csv(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV file is missing a header row")

        missing_columns = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing_columns:
            columns = ", ".join(missing_columns)
            raise ValueError(f"CSV file is missing required columns: {columns}")

        rows: list[dict[str, object]] = []
        for row in reader:
            row_with_number: dict[str, object] = dict(row)
            row_with_number[CSV_ROW_NUMBER_KEY] = reader.line_num
            rows.append(row_with_number)

    return rows


if __name__ == "__main__":
    raise SystemExit(main())
