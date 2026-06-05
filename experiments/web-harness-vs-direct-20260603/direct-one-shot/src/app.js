const STORAGE_KEY = "sprint-board-lite.tasks.v1";
const STATUSES = ["backlog", "doing", "review", "done"];
const PRIORITIES = ["low", "medium", "high"];

const STATUS_LABELS = {
  backlog: "Backlog",
  doing: "Doing",
  review: "Review",
  done: "Done",
};

const SAMPLE_TASKS = [
  {
    title: "Confirm sprint scope",
    owner: "Maya",
    effort: 2,
    priority: "high",
    status: "backlog",
    notes: "Trim carryover before planning.",
  },
  {
    title: "Build auth error state",
    owner: "Nina",
    effort: 3,
    priority: "medium",
    status: "doing",
    notes: "Cover locked and expired sessions.",
  },
  {
    title: "Review release checklist",
    owner: "Owen",
    effort: 1,
    priority: "low",
    status: "review",
    notes: "Verify owners for each launch step.",
  },
  {
    title: "Publish sprint notes",
    owner: "Maya",
    effort: 1,
    priority: "medium",
    status: "done",
    notes: "Share summary with the team.",
  },
];

const state = {
  tasks: [],
  filters: {
    search: "",
    status: "all",
    owner: "all",
  },
};

function getStorage() {
  try {
    if (typeof localStorage !== "undefined") {
      return localStorage;
    }
  } catch (error) {
    return null;
  }
  return null;
}

function createId() {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `task-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
}

function normalizeChoice(value, allowed, fallback) {
  const normalized = String(value || "").trim().toLowerCase();
  return allowed.includes(normalized) ? normalized : fallback;
}

function cloneSampleTasks() {
  return SAMPLE_TASKS.map((task) => normalizeTask(task));
}

function getTaskListFromImport(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (value && Array.isArray(value.tasks)) {
    return value.tasks;
  }
  throw new Error("Expected a JSON array or an object with a tasks array.");
}

function formatEffort(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return "0";
  }
  return Number.isInteger(number) ? String(number) : number.toFixed(1);
}

function setMessage(message, isError = false) {
  if (typeof document === "undefined") {
    return;
  }
  const element = document.querySelector("#app-message");
  if (!element) {
    return;
  }
  element.textContent = message;
  element.classList.toggle("error", isError);
}

function syncFiltersFromDom() {
  if (typeof document === "undefined") {
    return;
  }
  const searchInput = document.querySelector("#search-input");
  const statusFilter = document.querySelector("#status-filter");
  const ownerFilter = document.querySelector("#owner-filter");
  state.filters.search = searchInput ? searchInput.value : "";
  state.filters.status = statusFilter ? statusFilter.value : "all";
  state.filters.owner = ownerFilter ? ownerFilter.value : "all";
}

function renderMetrics(tasks) {
  const metrics = calculateMetrics(tasks);
  const total = document.querySelector("#metric-total");
  const completion = document.querySelector("#metric-completion");
  const effort = document.querySelector("#metric-effort");
  const highPriority = document.querySelector("#metric-high-priority");

  if (total) {
    total.textContent = String(metrics.totalTasks);
  }
  if (completion) {
    completion.textContent = `${metrics.completionPercentage}%`;
  }
  if (effort) {
    effort.textContent = formatEffort(metrics.totalEffort);
  }
  if (highPriority) {
    highPriority.textContent = String(metrics.openHighPriority);
  }
}

function renderOwnerFilter(tasks) {
  const select = document.querySelector("#owner-filter");
  if (!select) {
    return;
  }

  const currentValue = state.filters.owner || select.value || "all";
  const owners = [...new Set(tasks.map(normalizeTask).filter((task) => task.title).map((task) => task.owner))]
    .sort((a, b) => a.localeCompare(b));

  select.innerHTML = "";
  const allOption = document.createElement("option");
  allOption.value = "all";
  allOption.textContent = "All";
  select.appendChild(allOption);

  owners.forEach((owner) => {
    const option = document.createElement("option");
    option.value = owner;
    option.textContent = owner;
    select.appendChild(option);
  });

  select.value = owners.includes(currentValue) ? currentValue : "all";
  state.filters.owner = select.value;
}

function createMetaItem(label, value) {
  const item = document.createElement("span");
  const key = document.createElement("b");
  key.textContent = `${label}: `;
  item.appendChild(key);

  if (value instanceof Node) {
    item.appendChild(value);
  } else {
    item.appendChild(document.createTextNode(value));
  }
  return item;
}

function createStatusSelect(task) {
  const wrapper = document.createElement("div");
  const safeId = task.id.replace(/[^a-z0-9_-]/gi, "-");
  const label = document.createElement("label");
  const select = document.createElement("select");

  select.id = `status-${safeId}`;
  select.className = "card-status";
  select.dataset.taskId = task.id;
  select.value = task.status;

  STATUSES.forEach((status) => {
    const option = document.createElement("option");
    option.value = status;
    option.textContent = STATUS_LABELS[status];
    option.selected = status === task.status;
    select.appendChild(option);
  });

  label.htmlFor = select.id;
  label.textContent = "Status";
  wrapper.append(label, select);
  return wrapper;
}

function createTaskCard(task) {
  const card = document.createElement("article");
  card.className = `task-card priority-${task.priority}`;
  card.dataset.taskId = task.id;

  const title = document.createElement("h3");
  title.className = "task-title";
  title.textContent = task.title;

  const priority = document.createElement("span");
  priority.className = `priority-badge ${task.priority}`;
  priority.textContent = task.priority;

  const meta = document.createElement("div");
  meta.className = "task-meta";
  meta.append(
    createMetaItem("Owner", task.owner),
    createMetaItem("Effort", formatEffort(task.effort)),
    createMetaItem("Priority", priority),
    createMetaItem("Status", STATUS_LABELS[task.status])
  );

  const notes = document.createElement("p");
  notes.className = "task-notes";
  notes.textContent = task.notes || "No notes";

  const controls = document.createElement("div");
  controls.className = "card-controls";
  controls.appendChild(createStatusSelect(task));

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-task";
  deleteButton.type = "button";
  deleteButton.dataset.taskId = task.id;
  deleteButton.textContent = "Delete";
  controls.appendChild(deleteButton);

  card.append(title, meta, notes, controls);
  return card;
}

function createEmptyState(status) {
  const empty = document.createElement("p");
  empty.className = "empty-state";
  empty.textContent = `No ${STATUS_LABELS[status].toLowerCase()} tasks`;
  return empty;
}

function addTask(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const titleInput = document.querySelector("#task-title");
  const rawTitle = titleInput ? titleInput.value : "";

  if (!rawTitle.trim()) {
    setMessage("Title required.", true);
    if (titleInput) {
      titleInput.focus();
    }
    return;
  }

  const data = new FormData(form);
  const task = normalizeTask({
    title: data.get("title"),
    owner: data.get("owner"),
    effort: data.get("effort"),
    priority: data.get("priority"),
    status: data.get("status"),
    notes: data.get("notes"),
  });

  state.tasks = saveTasks([...state.tasks, task]);
  form.reset();
  document.querySelector("#task-effort").value = "1";
  document.querySelector("#task-priority").value = "medium";
  document.querySelector("#task-status").value = "backlog";
  renderBoard();
  setMessage("Task added.");
}

function updateTaskStatus(taskId, nextStatus) {
  const status = normalizeChoice(nextStatus, STATUSES, "backlog");
  state.tasks = saveTasks(
    state.tasks.map((task) => (task.id === taskId ? normalizeTask({ ...task, status }) : task))
  );
  renderBoard();
  setMessage("Status updated.");
}

function deleteTask(taskId) {
  state.tasks = saveTasks(state.tasks.filter((task) => task.id !== taskId));
  renderBoard();
  setMessage("Task deleted.");
}

function handleBoardChange(event) {
  const target = event.target;
  if (target && target.classList.contains("card-status")) {
    updateTaskStatus(target.dataset.taskId, target.value);
  }
}

function handleBoardClick(event) {
  const target = event.target;
  if (target && target.classList.contains("delete-task")) {
    deleteTask(target.dataset.taskId);
  }
}

function exportJson() {
  const output = document.querySelector("#export-output");
  if (!output) {
    return;
  }
  output.value = JSON.stringify(state.tasks, null, 2);
  output.focus();
  output.select();
  setMessage("Export ready.");
}

function importJsonFromFile(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();
  reader.addEventListener("load", () => {
    try {
      const parsed = JSON.parse(String(reader.result || ""));
      const importedTasks = getTaskListFromImport(parsed).map(normalizeTask).filter((task) => task.title);
      state.tasks = saveTasks(importedTasks);
      renderBoard();
      setMessage("Import complete.");
    } catch (error) {
      setMessage("Import failed.", true);
    } finally {
      event.target.value = "";
    }
  });
  reader.readAsText(file);
}

function bindEvents() {
  const form = document.querySelector("#task-form");
  const searchInput = document.querySelector("#search-input");
  const statusFilter = document.querySelector("#status-filter");
  const ownerFilter = document.querySelector("#owner-filter");
  const board = document.querySelector("#board");
  const exportButton = document.querySelector("#export-json");
  const importButton = document.querySelector("#import-json");
  const importFile = document.querySelector("#import-file");

  if (form) {
    form.addEventListener("submit", addTask);
  }
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      syncFiltersFromDom();
      renderBoard();
    });
  }
  if (statusFilter) {
    statusFilter.addEventListener("change", () => {
      syncFiltersFromDom();
      renderBoard();
    });
  }
  if (ownerFilter) {
    ownerFilter.addEventListener("change", () => {
      syncFiltersFromDom();
      renderBoard();
    });
  }
  if (board) {
    board.addEventListener("change", handleBoardChange);
    board.addEventListener("click", handleBoardClick);
  }
  if (exportButton) {
    exportButton.addEventListener("click", exportJson);
  }
  if (importButton && importFile) {
    importButton.addEventListener("click", () => importFile.click());
  }
  if (importFile) {
    importFile.addEventListener("change", importJsonFromFile);
  }
}

function startApp() {
  const app = document.querySelector("#app");
  if (!app) {
    return;
  }
  state.tasks = loadTasks();
  syncFiltersFromDom();
  bindEvents();
  renderBoard();
  app.dataset.ready = "true";
}

export function normalizeTask(task = {}) {
  const source = task && typeof task === "object" ? task : {};
  const title = String(source.title || "").trim();
  const owner = String(source.owner || "").trim() || "Unassigned";
  const effortValue = Number(source.effort);
  const effort = Number.isFinite(effortValue) && effortValue >= 0 ? effortValue : 0;
  const status = normalizeChoice(source.status, STATUSES, "backlog");
  const priority = normalizeChoice(source.priority, PRIORITIES, "medium");
  const notes = String(source.notes || "").trim();
  const id = String(source.id || "").trim() || createId();
  const createdAt = String(source.createdAt || "").trim() || new Date().toISOString();

  return {
    id,
    title,
    owner,
    effort,
    priority,
    status,
    notes,
    createdAt,
  };
}

export function calculateMetrics(tasks = []) {
  const normalizedTasks = tasks.map(normalizeTask).filter((task) => task.title);
  const totalTasks = normalizedTasks.length;
  const doneTasks = normalizedTasks.filter((task) => task.status === "done").length;
  const totalEffort = normalizedTasks.reduce((sum, task) => sum + task.effort, 0);
  const openHighPriority = normalizedTasks.filter(
    (task) => task.priority === "high" && task.status !== "done"
  ).length;
  const completionPercentage = totalTasks === 0 ? 0 : Math.round((doneTasks / totalTasks) * 100);

  return {
    totalTasks,
    completionPercentage,
    totalEffort,
    openHighPriority,
  };
}

export function filterTasks(tasks = [], filters = {}) {
  const search = String(filters.search || "").trim().toLowerCase();
  const status = String(filters.status || "all");
  const owner = String(filters.owner || "all");

  return tasks
    .map(normalizeTask)
    .filter((task) => task.title)
    .filter((task) => status === "all" || task.status === status)
    .filter((task) => owner === "all" || task.owner === owner)
    .filter((task) => {
      if (!search) {
        return true;
      }
      return [task.title, task.owner, task.notes, task.priority, task.status]
        .join(" ")
        .toLowerCase()
        .includes(search);
    });
}

export function saveTasks(tasks = []) {
  const normalizedTasks = tasks.map(normalizeTask).filter((task) => task.title);
  const storage = getStorage();
  if (storage) {
    storage.setItem(STORAGE_KEY, JSON.stringify(normalizedTasks));
  }
  return normalizedTasks;
}

export function loadTasks() {
  const storage = getStorage();
  if (!storage) {
    return cloneSampleTasks();
  }

  const rawTasks = storage.getItem(STORAGE_KEY);
  if (rawTasks === null) {
    const seededTasks = cloneSampleTasks();
    storage.setItem(STORAGE_KEY, JSON.stringify(seededTasks));
    return seededTasks;
  }

  try {
    return getTaskListFromImport(JSON.parse(rawTasks)).map(normalizeTask).filter((task) => task.title);
  } catch (error) {
    return [];
  }
}

export function renderBoard(tasks = state.tasks) {
  if (typeof document === "undefined") {
    return;
  }

  renderOwnerFilter(tasks);
  const visibleTasks = filterTasks(tasks, state.filters);
  renderMetrics(visibleTasks);

  document.querySelectorAll(".column[data-status]").forEach((column) => {
    const status = column.dataset.status;
    const list = column.querySelector(".task-list");
    if (!list || !STATUSES.includes(status)) {
      return;
    }

    const columnTasks = visibleTasks.filter((task) => task.status === status);
    list.innerHTML = "";

    if (columnTasks.length === 0) {
      list.appendChild(createEmptyState(status));
      return;
    }

    columnTasks.forEach((task) => {
      list.appendChild(createTaskCard(task));
    });
  });
}

if (typeof window !== "undefined") {
  window.SprintBoardLite = {
    normalizeTask,
    calculateMetrics,
    filterTasks,
    saveTasks,
    loadTasks,
    renderBoard,
  };
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startApp);
  } else {
    startApp();
  }
}
