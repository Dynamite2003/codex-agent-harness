from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.labels_for: set[str] = set()
        self.data_statuses: set[str] = set()
        self.scripts: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.buttons: list[str] = []
        self.current_button: list[str] | None = None
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if "id" in attr:
            self.ids.add(attr["id"])
        if tag == "label" and "for" in attr:
            self.labels_for.add(attr["for"])
        if "data-status" in attr:
            self.data_statuses.add(attr["data-status"])
        if tag == "script":
            self.scripts.append(attr)
        if tag == "link":
            self.links.append(attr)
        if tag == "button":
            self.current_button = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "button" and self.current_button is not None:
            self.buttons.append(" ".join(self.current_button).strip())
            self.current_button = None

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.text_parts.append(text)
            if self.current_button is not None:
                self.current_button.append(text)


class StaticWebContractTests(unittest.TestCase):
    def _parse_html(self) -> ContractParser:
        parser = ContractParser()
        parser.feed((PROJECT_ROOT / "index.html").read_text(encoding="utf-8"))
        return parser

    def test_expected_files_exist(self) -> None:
        for relative_path in ["index.html", "src/app.js", "src/styles.css"]:
            self.assertTrue((PROJECT_ROOT / relative_path).exists(), relative_path)

    def test_html_declares_app_shell(self) -> None:
        parser = self._parse_html()
        required_ids = {
            "app",
            "task-form",
            "task-title",
            "task-owner",
            "task-effort",
            "task-priority",
            "task-status",
            "task-notes",
            "search-input",
            "status-filter",
            "owner-filter",
            "metric-total",
            "metric-completion",
            "metric-effort",
            "metric-high-priority",
            "export-json",
            "import-json",
            "import-file",
        }
        self.assertTrue(required_ids.issubset(parser.ids), sorted(required_ids - parser.ids))
        self.assertTrue(
            {
                "task-title",
                "task-owner",
                "task-effort",
                "task-priority",
                "task-status",
                "task-notes",
                "search-input",
                "status-filter",
                "owner-filter",
            }.issubset(parser.labels_for)
        )
        self.assertEqual({"backlog", "doing", "review", "done"}, parser.data_statuses)
        self.assertTrue(any(link.get("href") == "src/styles.css" for link in parser.links))
        self.assertTrue(
            any(script.get("src") == "src/app.js" and script.get("type") == "module" for script in parser.scripts)
        )
        text = " ".join(parser.text_parts)
        for expected in ["Sprint Board Lite", "Backlog", "Doing", "Review", "Done"]:
            self.assertIn(expected, text)

    def test_html_does_not_depend_on_external_assets(self) -> None:
        html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotRegex(html, r"https?://|//cdn\.|fonts\.googleapis")

    def test_javascript_contract(self) -> None:
        js = (PROJECT_ROOT / "src" / "app.js").read_text(encoding="utf-8")
        for name in [
            "normalizeTask",
            "calculateMetrics",
            "filterTasks",
            "saveTasks",
            "loadTasks",
            "renderBoard",
        ]:
            self.assertRegex(js, rf"\bfunction\s+{name}\b|export\s+function\s+{name}\b|const\s+{name}\s=")
        for snippet in [
            "sprint-board-lite.tasks.v1",
            "localStorage",
            "addEventListener",
            "JSON.stringify",
            "JSON.parse",
            "querySelector",
            "data-status",
        ]:
            self.assertIn(snippet, js)
        self.assertRegex(js, r"typeof\s+document\s*!==\s*['\"]undefined['\"]")
        self.assertRegex(js, r"backlog|doing|review|done")
        self.assertRegex(js, r"low|medium|high")

    def test_css_contract(self) -> None:
        css = (PROJECT_ROOT / "src" / "styles.css").read_text(encoding="utf-8")
        for selector_hint in [
            ".board",
            ".column",
            ".task-card",
            ".metrics",
            ".filters",
            ".empty-state",
        ]:
            self.assertIn(selector_hint, css)
        self.assertIn("@media", css)
        self.assertRegex(css, r":focus|:focus-visible")
        self.assertRegex(css, r"grid|flex")

    def test_task_form_controls_are_not_placeholder_only(self) -> None:
        html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"<input\b|<select\b|<textarea\b", html)), 8)
        parser = self._parse_html()
        self.assertTrue(any("Export" in label for label in parser.buttons))
        self.assertTrue(any("Import" in label for label in parser.buttons))


if __name__ == "__main__":
    unittest.main()
