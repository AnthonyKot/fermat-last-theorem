/* No Such Form — theme toggle + KaTeX auto-render bootstrap.
   Vanilla JS, no dependencies beyond KaTeX (loaded from CDN in each page). */

(function () {
  var KEY = "nosuchform-theme";
  var root = document.documentElement;

  // Apply saved preference as early as possible.
  try {
    var saved = localStorage.getItem(KEY);
    if (saved === "light" || saved === "dark") {
      root.setAttribute("data-theme", saved);
    }
  } catch (e) { /* localStorage may be unavailable */ }

  function currentTheme() {
    var attr = root.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem(KEY, t); } catch (e) {}
    updateLabel(t);
  }

  function updateLabel(t) {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    var dark = t === "dark";
    btn.textContent = dark ? "☀ Light" : "☾ Dark";
    btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      updateLabel(currentTheme());
      btn.addEventListener("click", function () {
        setTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    }

    // Render TeX written as $…$ and $$…$$ once the page is ready.
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$",  right: "$",  display: false }
        ],
        throwOnError: false
      });
    }
  });
})();
