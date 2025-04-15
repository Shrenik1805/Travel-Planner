// app/static/js/theme-toggle.js

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");
    const root = document.documentElement;
    const currentTheme = localStorage.getItem("theme");

    if (currentTheme) {
        root.setAttribute("data-theme", currentTheme);
    }

    toggleBtn.addEventListener("click", () => {
        const newTheme = root.getAttribute("data-theme") === "light" ? "dark" : "light";
        root.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    });
});
