const STORAGE_KEY = "sprint-board-lite.tasks.v1";

function init() {
  const root = document.querySelector("main");
  if (root) {
    root.dataset.ready = "false";
  }
}

if (typeof document !== "undefined") {
  init();
}
