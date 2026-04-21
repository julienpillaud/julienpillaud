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

window.showToast = (message, options = {}) => {
  const {
    type = "error",
    timeout = 5000,
  } = options;

  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, timeout);
};
