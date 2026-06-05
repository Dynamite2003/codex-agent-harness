# Experiment Task: Expense Digest CLI

Build a small Python package named `expense_digest`.

The project already has a minimal Python package layout and a unittest test suite. Implement the application until the tests pass, and add any extra focused tests you think are useful.

Requirements:

- Provide library functions in `src/expense_digest/core.py`.
- Support summarizing rows with fields `date`, `category`, `amount`, and `description`.
- Treat blank or whitespace-only categories as `Uncategorized`.
- Parse amounts with `decimal.Decimal` and round output totals to two decimal places using standard money-style half-up rounding.
- `summarize_expenses(rows, min_amount=0.0, currency="USD")` should return:
  - `currency`: uppercase currency code.
  - `count`: number of rows included after filtering.
  - `grand_total`: numeric total rounded to 2 decimals.
  - `categories`: mapping from category name to numeric total rounded to 2 decimals.
- `min_amount` filters out rows whose parsed amount is lower than the threshold.
- Invalid or missing amounts should raise `ValueError` with a message that includes the CSV row number when that information is available.
- Provide a CLI via `python -m expense_digest`:
  - Positional argument: CSV file path.
  - Options: `--min-amount FLOAT`, `--currency CODE`, `--pretty`.
  - Output JSON to stdout.
  - Print user-facing errors to stderr and exit non-zero for invalid input.
- Keep the implementation dependency-free and compatible with Python 3.11.

Verification:

- Run `PYTHONPATH=src python3 -m unittest discover -s tests`.
- Run at least one manual CLI smoke test.
