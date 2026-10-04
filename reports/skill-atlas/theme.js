"use strict";

(() => {
  const root = document.documentElement;
  const storageKey = "skill-atlas-theme";
  let theme = "dark";

  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === "light" || saved === "dark") theme = saved;
  } catch {}

  root.dataset.theme = theme;

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#theme-toggle");
    const updateButton = () => {
      const label = root.dataset.theme === "dark" ? "Modo claro" : "Modo nocturno";
      button.textContent = label;
      button.setAttribute("aria-label", `Activar ${label.toLowerCase()}`);
    };

    updateButton();
    button.hidden = false;
    button.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      updateButton();
      try {
        localStorage.setItem(storageKey, next);
      } catch {}
    });
  });
})();
