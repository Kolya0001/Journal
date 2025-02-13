document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    // Проверяем, есть ли сохранённая тема в localStorage
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-theme");
    }

    // Переключение темы
    themeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-theme");

        // Сохранение состояния в localStorage
        if (body.classList.contains("dark-theme")) {
            localStorage.setItem("darkMode", "enabled");
        } else {
            localStorage.removeItem("darkMode");
        }
    });
});
