# Sprint Board Lite Experiment

This static web scaffold is used to compare one-shot Codex implementation against the local Codex Agent Harness flow.

Task details live in `../task.md`.

## App notes

Sprint Board Lite is a dependency-free static board. It stores tasks in browser
`localStorage` under `sprint-board-lite.tasks.v1` and seeds sample tasks only
when that key is empty.

Serve the directory with any static file server, then open the site in a
browser. For example:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`. Add tasks from the left panel, filter by
search/status/owner, move cards with each card's status control, and use the
JSON controls to export or import task data.

Run the contract tests with:

```bash
python3 -m unittest discover -s tests
```
