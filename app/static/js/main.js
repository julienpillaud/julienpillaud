document.addEventListener("DOMContentLoaded", () => {
  const themeController = document.querySelector('.theme-controller');
  const currentTheme = localStorage.getItem('theme');
  themeController.checked = currentTheme === themeController.value;
  themeController.addEventListener("change", (event) => {
    const selectedTheme = event.target.checked ? event.target.value : "light";
    document.documentElement.setAttribute("data-theme", selectedTheme);
    localStorage.setItem("theme", selectedTheme);
  })
});
