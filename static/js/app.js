/**
 * app.js - Client-Side Interactive Logic for BuyerGuard BD
 * Manages pre-purchase checklist state, local storage persistence,
 * real-time table filtering, and print triggers.
 */

document.addEventListener("DOMContentLoaded", () => {
  initChecklist();
  initTableQuickSearch();
  initPrintTriggers();
  initHaqShufaForm();
});

/**
 * Initializes the interactive Pre-Purchase Citizen Checklist.
 * Supports persistent completion storage in localStorage.
 */
function initChecklist() {
  const checklistContainer = document.getElementById("verification-checklist");
  if (!checklistContainer) return;

  const plotId = checklistContainer.getAttribute("data-plot-id") || "global";
  const storageKey = `buyerguard_checklist_${plotId}`;
  const checkboxes = checklistContainer.querySelectorAll(".checklist-checkbox");
  const countDisplay = document.getElementById("checklist-completed-count");
  const totalDisplay = document.getElementById("checklist-total-count");
  const progressBar = document.getElementById("checklist-progress-bar");
  const resetBtn = document.getElementById("checklist-reset-btn");

  if (totalDisplay) {
    totalDisplay.textContent = checkboxes.length;
  }

  // Load stored state
  let savedState = {};
  try {
    const raw = localStorage.getItem(storageKey);
    if (raw) savedState = JSON.parse(raw);
  } catch (e) {
    console.warn("Could not read localStorage for checklist:", e);
  }

  // Apply stored state
  checkboxes.forEach((cb) => {
    const itemId = cb.getAttribute("data-item-id");
    if (savedState[itemId]) {
      cb.checked = true;
      const parent = cb.closest(".checklist-item");
      if (parent) parent.classList.add("completed");
    }

    // Attach change listener
    cb.addEventListener("change", () => {
      const parent = cb.closest(".checklist-item");
      if (cb.checked) {
        if (parent) parent.classList.add("completed");
        savedState[itemId] = true;
      } else {
        if (parent) parent.classList.remove("completed");
        delete savedState[itemId];
      }

      try {
        localStorage.setItem(storageKey, JSON.stringify(savedState));
      } catch (e) {
        console.warn("Could not persist checklist to localStorage:", e);
      }

      updateProgress();
    });
  });

  // Reset button
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      checkboxes.forEach((cb) => {
        cb.checked = false;
        const parent = cb.closest(".checklist-item");
        if (parent) parent.classList.remove("completed");
      });
      savedState = {};
      try {
        localStorage.removeItem(storageKey);
      } catch (e) {
        console.warn("Could not clear localStorage:", e);
      }
      updateProgress();
    });
  }

  function updateProgress() {
    let completed = 0;
    checkboxes.forEach((cb) => {
      if (cb.checked) completed++;
    });

    if (countDisplay) countDisplay.textContent = completed;
    if (progressBar) {
      const total = checkboxes.length || 1;
      const percent = Math.round((completed / total) * 100);
      progressBar.style.width = `${percent}%`;
      progressBar.setAttribute("aria-valuenow", percent);
    }
  }

  // Initial progress update
  updateProgress();
}

/**
 * Initializes instant table filtering for the dashboard.
 */
function initTableQuickSearch() {
  const searchInput = document.getElementById("table-quick-search");
  const tableBody = document.getElementById("plots-table-body");
  if (!searchInput || !tableBody) return;

  const rows = tableBody.querySelectorAll(".plot-record-row");
  const emptyState = document.getElementById("quick-search-empty");
  const liveStatus = document.getElementById("table-search-status");

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase().trim();
    let visibleCount = 0;

    rows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      if (text.includes(term)) {
        row.style.display = "";
        visibleCount += 1;
      } else {
        row.style.display = "none";
      }
    });

    if (emptyState) {
      emptyState.hidden = term.length === 0 || visibleCount > 0;
    }

    if (liveStatus) {
      const label = term ? liveStatus.dataset.matchingLabel : liveStatus.dataset.totalLabel;
      liveStatus.textContent = `${term ? visibleCount : rows.length} ${label || ""}`.trim();
    }
  });
}

/**
 * Connects print buttons to browser print dialog.
 */
function initPrintTriggers() {
  const printButtons = document.querySelectorAll('[data-action="print-report"]');
  printButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      window.print();
    });
  });
}

/**
 * Initializes interactive behaviors for the Haq Shufa Assessment form.
 */
function initHaqShufaForm() {
  const resetBtn = document.getElementById("haq-shufa-reset-btn");
  const resultsCard = document.getElementById("haq-shufa-results-card");
  if (resetBtn && resultsCard) {
    resetBtn.addEventListener("click", () => {
      resultsCard.style.display = "none";
    });
  }
}

