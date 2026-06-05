const STORAGE_KEY = "sprint-board-lite.tasks.v1";
const ALL_FILTER = "All";

const STATUSES = ["backlog", "doing", "review", "done"];
const PRIORITIES = ["low", "medium", "high"];

const STATUS_LABELS = {
  backlog: "Backlog",
  doing: "Doing",
  review: "Review",
  done: "Done",
};

const PRIORITY_LABELS = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

const appState = {
  tasks: [],
  filters: {
    query: "",
    status: ALL_FILTER,
    owner: ALL_FILTER,
  },
};

let idCounter = 0;
let eventsBound = false;

function createTaskId() {
  idCounter += 1;
  return `task-${Date.now()}-${idCounter}`;
}

function toTrimmedString(value) {
  if (value === null || value === undefined) {
    return "";
  }
  return String(value).trim();
}

function normalizeEffort(value) {
  if (value === "" || value === null || value === undefined) {
    return 0;
  }
  const effort = Number(value);
  if (!Number.isFinite(effort) || effort < 0) {
    return 0;
  }
  return effort;
}

function normalizeTaskList(tasks) {
  if (!Array.isArray(tasks)) {
    return [];
  }
  return tasks.map((task) => normalizeTask(task)).filter((task) => task.title.length > 0);
}

function getStorage() {
  try {
    if (typeof globalThis !== "undefined" && "localStorage" in globalThis) {
      return globalThis.localStorage;
    }
  } catch (error) {
    return null;
  }
  return null;
}

function getSampleTasks() {
  return normalizeTaskList([
    {
      id: "sample-backlog",
      title: "Define sprint goals",
      owner: "Mina",
      effort: 2,
      priority: "high",
      status: "backlog",
      notes: "Confirm scope with the team before planning.",
    },
    {
      id: "sample-doing",
      title: "Build task form",
      owner: "Alex",
      effort: 3,
      priority: "medium",
      status: "doing",
      notes: "Keep the form compact and keyboard friendly.",
    },
    {
      id: "sample-review",
      title: "Review import flow",
      owner: "Priya",
      effort: 1,
      priority: "low",
      status: "review",
      notes: "Check array and object import formats.",
    },
    {
      id: "sample-done",
      title: "Set up static shell",
      owner: "Unassigned",
      effort: 1,
      priority: "medium",
      status: "done",
      notes: "HTML, CSS, and JavaScript are served directly.",
    },
  ]);
}

function setText(id, value) {
  if (typeof document === "undefined") {
    return;
  }
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
}

function setFeedback(message, tone = "neutral") {
  if (typeof document === "undefined") {
    return;
  }
  const feedback = document.getElementById("feedback");
  if (!feedback) {
    return;
  }
  feedback.textContent = message;
  feedback.dataset.tone = tone;
}

function createElement(tagName, options = {}) {
  const element = document.createElement(tagName);
  if (options.className) {
    element.className = options.className;
  }
  if (options.text !== undefined) {
    element.textContent = options.text;
  }
  if (options.attributes) {
    Object.entries(options.attributes).forEach(([name, value]) => {
      element.setAttribute(name, value);
    });
  }
  return element;
}

function createOption(value, label, selectedValue) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  option.selected = value === selectedValue;
  return option;
}

function getOwnerOptions(tasks) {
  const owners = normalizeTaskList(tasks).map((task) => task.owner);
  return [ALL_FILTER, ...Array.from(new Set(owners)).sort((a, b) => a.localeCompare(b))];
}

function ensureValidFilters(tasks, filters) {
  const nextFilters = {
    query: toTrimmedString(filters?.query),
    status: STATUSES.includes(filters?.status) ? filters.status : ALL_FILTER,
    owner: toTrimmedString(filters?.owner) || ALL_FILTER,
  };
  const ownerOptions = getOwnerOptions(tasks);
  if (!ownerOptions.includes(nextFilters.owner)) {
    nextFilters.owner = ALL_FILTER;
  }
  return nextFilters;
}

function renderOwnerFilter(tasks, filters) {
  const ownerFilter = document.getElementById("owner-filter");
  if (!ownerFilter) {
    return filters;
  }

  const ownerOptions = getOwnerOptions(tasks);
  const selectedOwner = ownerOptions.includes(filters.owner) ? filters.owner : ALL_FILTER;
  if (filters.owner !== selectedOwner) {
    filters.owner = selectedOwner;
  }

  ownerFilter.innerHTML = "";
  ownerOptions.forEach((owner) => {
    ownerFilter.append(createOption(owner, owner, selectedOwner));
  });
  ownerFilter.value = selectedOwner;
  return filters;
}

function createTaskCard(task) {
  const card = createElement("article", {
    className: "task-card",
    attributes: {
      "data-task-id": task.id,
      "data-priority": task.priority,
      "data-status": task.status,
    },
  });

  const header = createElement("div", { className: "task-card__header" });
  header.append(createElement("h3", { text: task.title }));

  const priority = createElement("span", {
    className: `task-pill task-pill--${task.priority}`,
    text: `${PRIORITY_LABELS[task.priority]} priority`,
  });
  header.append(priority);
  card.append(header);

  const details = createElement("dl", { className: "task-card__details" });
  [
    ["Owner", task.owner],
    ["Effort", String(task.effort)],
    ["Status", STATUS_LABELS[task.status]],
  ].forEach(([label, value]) => {
    details.append(createElement("dt", { text: label }));
    details.append(createElement("dd", { text: value }));
  });
  card.append(details);

  if (task.notes) {
    card.append(createElement("p", { className: "task-card__notes", text: task.notes }));
  }

  const actions = createElement("div", { className: "task-card__actions" });
  const statusLabel = createElement("label", {
    className: "sr-only",
    text: `Change status for ${task.title}`,
    attributes: { for: `status-${task.id}` },
  });
  const statusSelect = createElement("select", {
    className: "task-status-control",
    attributes: {
      id: `status-${task.id}`,
      "data-task-id": task.id,
      "aria-label": `Change status for ${task.title}`,
    },
  });
  STATUSES.forEach((status) => {
    statusSelect.append(createOption(status, STATUS_LABELS[status], task.status));
  });

  const deleteButton = createElement("button", {
    className: "task-delete",
    text: "Delete",
    attributes: {
      type: "button",
      "data-task-id": task.id,
      "aria-label": `Delete ${task.title}`,
    },
  });

  actions.append(statusLabel, statusSelect, deleteButton);
  card.append(actions);
  return card;
}

function downloadJson(filename, jsonText) {
  const blob = new Blob([jsonText], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.hidden = true;
  document.body.append(link);
  link.click();
  URL.revokeObjectURL(link.href);
  link.remove();
}

function parseImportedTasks(text) {
  const parsed = JSON.parse(text);
  const imported = Array.isArray(parsed) ? parsed : parsed?.tasks;
  if (!Array.isArray(imported)) {
    throw new Error("Import JSON must be an array or an object with a tasks array.");
  }
  return normalizeTaskList(imported);
}

export function normalizeTask(input = {}) {
  const source = input && typeof input === "object" ? input : {};
  const id = toTrimmedString(source.id) || createTaskId();
  const title = toTrimmedString(source.title);
  const owner = toTrimmedString(source.owner) || "Unassigned";
  const effort = normalizeEffort(source.effort);
  const priority = PRIORITIES.includes(source.priority) ? source.priority : "medium";
  const status = STATUSES.includes(source.status) ? source.status : "backlog";
  const notes = toTrimmedString(source.notes);

  return {
    id,
    title,
    owner,
    effort,
    priority,
    status,
    notes,
  };
}

export function calculateMetrics(tasks = []) {
  const normalizedTasks = normalizeTaskList(tasks);
  const total = normalizedTasks.length;
  const done = normalizedTasks.filter((task) => task.status === "done").length;
  const completionPercentage = total === 0 ? 0 : Math.round((done / total) * 100);
  const totalEffort = normalizedTasks.reduce((sum, task) => sum + task.effort, 0);
  const highPriorityOpen = normalizedTasks.filter(
    (task) => task.priority === "high" && task.status !== "done",
  ).length;

  return {
    total,
    completionPercentage,
    totalEffort,
    highPriorityOpen,
  };
}

export function filterTasks(tasks = [], filters = {}) {
  const normalizedTasks = normalizeTaskList(tasks);
  const query = toTrimmedString(filters.query).toLowerCase();
  const status = STATUSES.includes(filters.status) ? filters.status : ALL_FILTER;
  const owner = toTrimmedString(filters.owner) || ALL_FILTER;

  return normalizedTasks.filter((task) => {
    const matchesQuery =
      query.length === 0 ||
      [task.title, task.owner, task.notes].some((value) => value.toLowerCase().includes(query));
    const matchesStatus = status === ALL_FILTER || task.status === status;
    const matchesOwner = owner === ALL_FILTER || task.owner === owner;
    return matchesQuery && matchesStatus && matchesOwner;
  });
}

export function saveTasks(tasks = []) {
  const storage = getStorage();
  if (!storage) {
    return false;
  }

  try {
    storage.setItem(STORAGE_KEY, JSON.stringify(normalizeTaskList(tasks)));
    return true;
  } catch (error) {
    return false;
  }
}

export function loadTasks() {
  const storage = getStorage();
  if (!storage) {
    return getSampleTasks();
  }

  try {
    const stored = storage.getItem(STORAGE_KEY);
    if (stored === null) {
      const samples = getSampleTasks();
      storage.setItem(STORAGE_KEY, JSON.stringify(samples));
      return samples;
    }

    const parsed = JSON.parse(stored);
    return normalizeTaskList(Array.isArray(parsed) ? parsed : []);
  } catch (error) {
    return [];
  }
}

export function renderBoard(tasks = appState.tasks, filters = appState.filters) {
  if (typeof document === "undefined") {
    return;
  }

  appState.tasks = normalizeTaskList(tasks);
  appState.filters = ensureValidFilters(appState.tasks, filters);
  renderOwnerFilter(appState.tasks, appState.filters);

  const metrics = calculateMetrics(appState.tasks);
  setText("metric-total", String(metrics.total));
  setText("metric-completion", `${metrics.completionPercentage}%`);
  setText("metric-effort", String(metrics.totalEffort));
  setText("metric-high-priority", String(metrics.highPriorityOpen));

  const visibleTasks = filterTasks(appState.tasks, appState.filters);
  const tasksByStatus = Object.fromEntries(STATUSES.map((status) => [status, []]));
  visibleTasks.forEach((task) => {
    tasksByStatus[task.status].push(task);
  });

  STATUSES.forEach((status) => {
    const column = document.querySelector(`[data-status="${status}"]`);
    const taskList =
      document.querySelector(`[data-task-list="${status}"]`) || column?.querySelector(".task-list");
    if (!taskList) {
      return;
    }
    taskList.innerHTML = "";
    if (tasksByStatus[status].length === 0) {
      taskList.append(
        createElement("p", {
          className: "empty-state",
          text: "No visible tasks",
        }),
      );
      return;
    }
    tasksByStatus[status].forEach((task) => {
      taskList.append(createTaskCard(task));
    });
  });
}

function bindForm() {
  const form = document.getElementById("task-form");
  if (!form) {
    return;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const task = normalizeTask({
      title: document.getElementById("task-title")?.value,
      owner: document.getElementById("task-owner")?.value,
      effort: document.getElementById("task-effort")?.value,
      priority: document.getElementById("task-priority")?.value,
      status: document.getElementById("task-status")?.value,
      notes: document.getElementById("task-notes")?.value,
    });

    if (!task.title) {
      setFeedback("Add a task title before saving.", "error");
      return;
    }

    appState.tasks = [...appState.tasks, task];
    saveTasks(appState.tasks);
    form.reset();
    setFeedback("Task added.", "success");
    renderBoard(appState.tasks, appState.filters);
  });
}

function bindFilters() {
  const searchInput = document.getElementById("search-input");
  const statusFilter = document.getElementById("status-filter");
  const ownerFilter = document.getElementById("owner-filter");

  searchInput?.addEventListener("input", (event) => {
    appState.filters.query = event.target.value;
    renderBoard(appState.tasks, appState.filters);
  });

  statusFilter?.addEventListener("change", (event) => {
    appState.filters.status = event.target.value;
    renderBoard(appState.tasks, appState.filters);
  });

  ownerFilter?.addEventListener("change", (event) => {
    appState.filters.owner = event.target.value;
    renderBoard(appState.tasks, appState.filters);
  });
}

function bindBoardActions() {
  const board = document.querySelector(".board");
  if (!board) {
    return;
  }

  board.addEventListener("change", (event) => {
    const control = event.target.closest(".task-status-control");
    if (!control) {
      return;
    }
    const taskId = control.dataset.taskId;
    const nextStatus = STATUSES.includes(control.value) ? control.value : "backlog";
    appState.tasks = appState.tasks.map((task) =>
      task.id === taskId ? normalizeTask({ ...task, status: nextStatus }) : task,
    );
    saveTasks(appState.tasks);
    setFeedback("Task status updated.", "success");
    renderBoard(appState.tasks, appState.filters);
  });

  board.addEventListener("click", (event) => {
    const deleteButton = event.target.closest(".task-delete");
    if (!deleteButton) {
      return;
    }
    const taskId = deleteButton.dataset.taskId;
    appState.tasks = appState.tasks.filter((task) => task.id !== taskId);
    saveTasks(appState.tasks);
    setFeedback("Task deleted.", "success");
    renderBoard(appState.tasks, appState.filters);
  });
}

function bindJsonControls() {
  const exportButton = document.getElementById("export-json");
  const importButton = document.getElementById("import-json");
  const importFile = document.getElementById("import-file");

  exportButton?.addEventListener("click", () => {
    try {
      const jsonText = JSON.stringify(appState.tasks, null, 2);
      downloadJson("sprint-board-lite-tasks.json", jsonText);
      setFeedback("Tasks exported.", "success");
    } catch (error) {
      setFeedback("Export failed.", "error");
    }
  });

  importButton?.addEventListener("click", () => {
    importFile?.click();
  });

  importFile?.addEventListener("change", (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const reader = new FileReader();
    reader.addEventListener("load", () => {
      try {
        const importedTasks = parseImportedTasks(String(reader.result || ""));
        appState.tasks = importedTasks;
        appState.filters.owner = ALL_FILTER;
        saveTasks(appState.tasks);
        setFeedback("Tasks imported.", "success");
        renderBoard(appState.tasks, appState.filters);
      } catch (error) {
        setFeedback("Import failed. Use a task array or an object with a tasks array.", "error");
      } finally {
        event.target.value = "";
      }
    });
    reader.addEventListener("error", () => {
      setFeedback("Import failed. The file could not be read.", "error");
      event.target.value = "";
    });
    reader.readAsText(file);
  });
}

function init() {
  if (eventsBound) {
    return;
  }
  eventsBound = true;
  appState.tasks = loadTasks();
  appState.filters = {
    query: "",
    status: ALL_FILTER,
    owner: ALL_FILTER,
  };
  bindForm();
  bindFilters();
  bindBoardActions();
  bindJsonControls();
  renderBoard(appState.tasks, appState.filters);
}

if (typeof window !== "undefined") {
  window.SprintBoardLite = {
    normalizeTask,
    calculateMetrics,
    filterTasks,
    saveTasks,
    loadTasks,
    renderBoard,
    appState,
  };
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}
