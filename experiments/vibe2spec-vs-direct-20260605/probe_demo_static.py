from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HTML = ROOT / "examples" / "demo-project" / "index.html"


def main() -> int:
    html = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_HTML
    text = html.read_text(encoding="utf-8")
    checks = [
        ("page has todo form", 'id="todo-form"' in text),
        ("page has title input", 'id="title-input"' in text),
        ("page has due date input", 'id="due-input"' in text and 'type="date"' in text),
        ("page has list and empty state", 'id="todo-list"' in text and 'id="empty-state"' in text),
        ("uses localStorage persistence", "localStorage.getItem" in text and "localStorage.setItem" in text),
        ("has addTodo function", "function addTodo" in text),
        ("has toggleTodo function", "function toggleTodo" in text),
        ("has deleteTodo function", "function deleteTodo" in text),
        ("has isOverdue function", "function isOverdue" in text),
        (
            "isOverdue ignores completed tasks",
            bool(re.search(r"function isOverdue[\s\S]+!todo\.completed", text)),
        ),
        (
            "isOverdue compares due date against today",
            bool(re.search(r"function isOverdue[\s\S]+todo\.dueDate\s*<\s*today", text)),
        ),
        ("empty title validation exists", "!title" in text and "Task title is required" in text),
        ("submit uses date input value", bool(re.search(r"addTodo\(title,\s*dueInput\.value\)", text))),
        ("overdue badge is rendered", "Overdue" in text and "badge" in text),
        ("completion triggers rerender and save", "completed: !todo.completed" in text and "saveTodos()" in text),
        ("delete filters item and saves", "todos.filter" in text and "deleteTodo" in text),
    ]
    result = {
        "target": str(html),
        "passed": sum(1 for _, ok in checks if ok),
        "total": len(checks),
        "checks": [{"name": name, "ok": ok} for name, ok in checks],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] == result["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
