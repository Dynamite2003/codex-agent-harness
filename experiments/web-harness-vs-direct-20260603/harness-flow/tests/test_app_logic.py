from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_SOURCE = PROJECT_ROOT / "src" / "app.js"
STORAGE_KEY = "sprint-board-lite.tasks.v1"


def run_node_assertions(tmp_path: Path, script: str) -> None:
    node = shutil.which("node")
    assert node is not None

    app_module = tmp_path / "app-under-test.mjs"
    app_module.write_text(APP_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")

    runner = tmp_path / "runner.mjs"
    runner.write_text(script.replace("__APP_MODULE__", app_module.as_uri()), encoding="utf-8")

    completed = subprocess.run([node, str(runner)], capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr


def source_text() -> str:
    return APP_SOURCE.read_text(encoding="utf-8")


def test_normalize_task_rules(tmp_path: Path) -> None:
    if shutil.which("node") is not None:
        run_node_assertions(
            tmp_path,
            textwrap.dedent(
                """
                const mod = await import("__APP_MODULE__");
                function assertRule(condition, message) {
                  if (!condition) throw new Error(message);
                }

                const valid = mod.normalizeTask({
                  id: 42,
                  title: "  Write tests  ",
                  owner: "  Dana  ",
                  effort: "3.5",
                  priority: "high",
                  status: "review",
                  notes: "  cover logic  "
                });
                assertRule(valid.id === "42", "existing id is preserved as a string");
                assertRule(valid.title === "Write tests", "title is trimmed");
                assertRule(valid.owner === "Dana", "owner is trimmed");
                assertRule(valid.effort === 3.5, "effort is parsed");
                assertRule(valid.priority === "high", "valid priority is preserved");
                assertRule(valid.status === "review", "valid status is preserved");
                assertRule(valid.notes === "cover logic", "notes are trimmed");

                const fallback = mod.normalizeTask({
                  title: "   ",
                  owner: "   ",
                  effort: "-4",
                  priority: "urgent",
                  status: "blocked"
                });
                assertRule(fallback.title === "", "blank title stays blank for caller filtering");
                assertRule(fallback.owner === "Unassigned", "blank owner falls back");
                assertRule(fallback.effort === 0, "negative effort falls back");
                assertRule(fallback.priority === "medium", "invalid priority falls back");
                assertRule(fallback.status === "backlog", "invalid status falls back");

                const generated = mod.normalizeTask({ title: "Generated id" });
                assertRule(typeof generated.id === "string" && generated.id.length > 0, "id is generated");
                """
            ),
        )
        return

    source = source_text()
    assert "export function normalizeTask" in source
    assert "toTrimmedString(source.title)" in source
    assert '"Unassigned"' in source
    assert "Number.isFinite(effort)" in source
    assert "effort < 0" in source
    assert 'PRIORITIES.includes(source.priority) ? source.priority : "medium"' in source
    assert 'STATUSES.includes(source.status) ? source.status : "backlog"' in source
    assert "toTrimmedString(source.id) || createTaskId()" in source


def test_calculate_metrics_rules(tmp_path: Path) -> None:
    if shutil.which("node") is not None:
        run_node_assertions(
            tmp_path,
            textwrap.dedent(
                """
                const mod = await import("__APP_MODULE__");
                function assertRule(condition, message) {
                  if (!condition) throw new Error(message);
                }

                const empty = mod.calculateMetrics([]);
                assertRule(empty.total === 0, "empty total");
                assertRule(empty.completionPercentage === 0, "empty completion");
                assertRule(empty.totalEffort === 0, "empty effort");
                assertRule(empty.highPriorityOpen === 0, "empty high priority count");

                const partial = mod.calculateMetrics([
                  { title: "A", effort: 2, priority: "high", status: "done" },
                  { title: "B", effort: 3, priority: "high", status: "doing" },
                  { title: "C", effort: 5, priority: "low", status: "backlog" }
                ]);
                assertRule(partial.total === 3, "partial total");
                assertRule(partial.completionPercentage === 33, "partial completion");
                assertRule(partial.totalEffort === 10, "effort sum");
                assertRule(partial.highPriorityOpen === 1, "done high priority is not open");

                const done = mod.calculateMetrics([
                  { title: "A", effort: 1, status: "done" },
                  { title: "B", effort: 1, status: "done" }
                ]);
                assertRule(done.completionPercentage === 100, "all done completion");
                """
            ),
        )
        return

    source = source_text()
    assert "export function calculateMetrics" in source
    assert "const total = normalizedTasks.length" in source
    assert 'task.status === "done"' in source
    assert "Math.round((done / total) * 100)" in source
    assert "sum + task.effort" in source
    assert 'task.priority === "high" && task.status !== "done"' in source


def test_filter_tasks_rules(tmp_path: Path) -> None:
    if shutil.which("node") is not None:
        run_node_assertions(
            tmp_path,
            textwrap.dedent(
                """
                const mod = await import("__APP_MODULE__");
                function assertRule(condition, message) {
                  if (!condition) throw new Error(message);
                }
                const tasks = [
                  { title: "API polish", owner: "Dana", notes: "Review payload", status: "review" },
                  { title: "Board shell", owner: "Mina", notes: "layout", status: "doing" },
                  { title: "Export JSON", owner: "Dana", notes: "backup", status: "done" }
                ];

                assertRule(mod.filterTasks(tasks, { query: "api" }).length === 1, "search title");
                assertRule(mod.filterTasks(tasks, { query: "MINA" }).length === 1, "case-insensitive owner");
                assertRule(mod.filterTasks(tasks, { query: "payload" }).length === 1, "search notes");
                assertRule(mod.filterTasks(tasks, { status: "done" }).length === 1, "status filter");
                assertRule(mod.filterTasks(tasks, { owner: "Dana" }).length === 2, "owner filter");
                assertRule(
                  mod.filterTasks(tasks, { query: "json", status: "done", owner: "Dana" }).length === 1,
                  "combined filters"
                );
                """
            ),
        )
        return

    source = source_text()
    assert "export function filterTasks" in source
    assert ".toLowerCase()" in source
    assert "[task.title, task.owner, task.notes]" in source
    assert "matchesQuery && matchesStatus && matchesOwner" in source
    assert "status === ALL_FILTER || task.status === status" in source
    assert "owner === ALL_FILTER || task.owner === owner" in source


def test_save_and_load_tasks_rules(tmp_path: Path) -> None:
    if shutil.which("node") is not None:
        run_node_assertions(
            tmp_path,
            textwrap.dedent(
                f"""
                const store = new Map();
                globalThis.localStorage = {{
                  getItem(key) {{
                    return store.has(key) ? store.get(key) : null;
                  }},
                  setItem(key, value) {{
                    store.set(key, String(value));
                  }},
                  removeItem(key) {{
                    store.delete(key);
                  }},
                  clear() {{
                    store.clear();
                  }}
                }};

                const mod = await import("__APP_MODULE__");
                function assertRule(condition, message) {{
                  if (!condition) throw new Error(message);
                }}

                const seeded = mod.loadTasks();
                assertRule(seeded.length > 0, "missing key seeds sample tasks");
                assertRule(store.has("{STORAGE_KEY}"), "seed is persisted");

                store.set("{STORAGE_KEY}", "[]");
                assertRule(mod.loadTasks().length === 0, "empty array does not reseed");

                store.set("{STORAGE_KEY}", "{{bad json");
                assertRule(mod.loadTasks().length === 0, "damaged JSON does not reseed");

                store.set("{STORAGE_KEY}", JSON.stringify([
                  {{ title: "Valid", owner: "Kim", effort: 2 }},
                  {{ title: "   ", owner: "Nobody" }}
                ]));
                const restored = mod.loadTasks();
                assertRule(restored.length === 1, "invalid blank-title stored task is filtered");
                assertRule(restored[0].title === "Valid", "valid stored task remains");

                mod.saveTasks([
                  {{ title: "Saved", owner: "   ", effort: "4" }},
                  {{ title: "   ", owner: "Dropped" }}
                ]);
                const saved = JSON.parse(store.get("{STORAGE_KEY}"));
                assertRule(saved.length === 1, "save filters invalid tasks");
                assertRule(saved[0].owner === "Unassigned", "save normalizes tasks");
                assertRule(saved[0].effort === 4, "save persists normalized effort");
                """
            ),
        )
        return

    source = source_text()
    assert STORAGE_KEY in source
    assert "export function saveTasks" in source
    assert "export function loadTasks" in source
    assert "storage.setItem(STORAGE_KEY, JSON.stringify(normalizeTaskList(tasks)))" in source
    assert "stored === null" in source
    assert "getSampleTasks()" in source
    assert "JSON.parse(stored)" in source
    assert "return []" in source
