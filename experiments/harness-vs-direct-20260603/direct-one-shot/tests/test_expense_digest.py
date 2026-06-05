from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ExpenseDigestTests(unittest.TestCase):
    def test_summarize_groups_categories_with_filter_and_rounding(self) -> None:
        from expense_digest.core import summarize_expenses

        rows = [
            {"date": "2026-06-01", "category": "Food", "amount": "12.345", "description": "lunch"},
            {"date": "2026-06-02", "category": "Food", "amount": "7.655", "description": "snack"},
            {"date": "2026-06-02", "category": "Travel", "amount": "20", "description": "metro"},
            {"date": "2026-06-03", "category": "", "amount": "5", "description": "cash"},
        ]

        summary = summarize_expenses(rows, min_amount=7.0, currency="usd")

        self.assertEqual(
            summary,
            {
                "currency": "USD",
                "count": 3,
                "grand_total": 40.0,
                "categories": {
                    "Food": 20.0,
                    "Travel": 20.0,
                },
            },
        )

    def test_blank_categories_are_uncategorized(self) -> None:
        from expense_digest.core import summarize_expenses

        rows = [
            {"date": "2026-06-01", "category": "   ", "amount": "3.10", "description": ""},
            {"date": "2026-06-02", "category": "", "amount": "2.90", "description": ""},
        ]

        summary = summarize_expenses(rows)

        self.assertEqual(summary["categories"], {"Uncategorized": 6.0})
        self.assertEqual(summary["grand_total"], 6.0)
        self.assertEqual(summary["count"], 2)

    def test_invalid_amount_mentions_row_number(self) -> None:
        from expense_digest.core import summarize_expenses

        rows = [
            {"date": "2026-06-01", "category": "Food", "amount": "bad", "description": "lunch"},
        ]

        with self.assertRaisesRegex(ValueError, r"row 1.*amount"):
            summarize_expenses(rows)

    def test_rounding_is_half_up_after_summing(self) -> None:
        from expense_digest.core import summarize_expenses

        rows = [
            {"date": "2026-06-01", "category": "Fees", "amount": "0.005", "description": ""},
            {"date": "2026-06-02", "category": "Fees", "amount": "0.005", "description": ""},
            {"date": "2026-06-03", "category": "Tax", "amount": "1.005", "description": ""},
        ]

        summary = summarize_expenses(rows)

        self.assertEqual(summary["grand_total"], 1.02)
        self.assertEqual(summary["categories"], {"Fees": 0.01, "Tax": 1.01})

    def test_cli_outputs_pretty_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "expenses.csv"
            csv_path.write_text(
                "date,category,amount,description\n"
                "2026-06-01,Food,12.345,lunch\n"
                "2026-06-02,Food,7.655,snack\n"
                "2026-06-02,Travel,20,metro\n"
                "2026-06-03,,5,cash\n",
                encoding="utf-8",
            )
            env = dict(os.environ)
            env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "expense_digest",
                    str(csv_path),
                    "--min-amount",
                    "7",
                    "--currency",
                    "eur",
                    "--pretty",
                ],
                cwd=PROJECT_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("\n  ", completed.stdout)
        self.assertEqual(completed.stderr, "")
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "currency": "EUR",
                "count": 3,
                "grand_total": 40.0,
                "categories": {
                    "Food": 20.0,
                    "Travel": 20.0,
                },
                },
            )

    def test_cli_invalid_amount_reports_csv_row_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "expenses.csv"
            csv_path.write_text(
                "date,category,amount,description\n"
                "2026-06-01,Food,10,lunch\n"
                "2026-06-02,Travel,bad,metro\n",
                encoding="utf-8",
            )
            env = dict(os.environ)
            env["PYTHONPATH"] = str(PROJECT_ROOT / "src")

            completed = subprocess.run(
                [sys.executable, "-m", "expense_digest", str(csv_path)],
                cwd=PROJECT_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")
        self.assertRegex(completed.stderr, r"row 3.*amount")


if __name__ == "__main__":
    unittest.main()
