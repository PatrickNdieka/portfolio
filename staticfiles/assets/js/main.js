const menuToggleBtn = document.querySelector(".menu-toggle");
const navMenu = document.querySelector("#nav-menu");
menuToggleBtn.addEventListener("click", () => {
  navMenu.classList.toggle("show");
});

const themeToggleBtn = document.querySelector(".theme-toggle");
const currentTheme = localStorage.getItem("themeMode");
if (document.cookie.length != 0) {
  const cookieArray = document.cookie.split(";");
  cookieArray.forEach((item) => {
    if (item.includes("themeMode")) {
      document.documentElement.setAttribute(
        "data-theme-mode",
        item.split("=")[1]
      );
    }
  });
}

if (currentTheme == "dark") {
  document.documentElement.setAttribute("data-theme-mode", "dark");
} else if (currentTheme == "light") {
  document.documentElement.setAttribute("data-theme-mode", "light");
}

themeToggleBtn.addEventListener("click", (e) => {
  if (window.getComputedStyle(e.target, "::after").content.includes("dark")) {
    document.documentElement.setAttribute("data-theme-mode", "dark");
    document.cookie = "themeMode=dark";
  } else if (
    window.getComputedStyle(e.target, "::after").content.includes("light")
  ) {
    document.documentElement.setAttribute("data-theme-mode", "light");
    document.cookie = "themeMode=light";
  }
});

const navigation = document.querySelector(".nav");
if (navigation.getBoundingClientRect().top == 0) {
  navigation.classList.add("scrollable");
} else {
  navigation.classList.remove("scrollable");
}
window.addEventListener("scroll", () => {
  if (navigation.getBoundingClientRect().top == 0) {
    navigation.classList.add("scrollable");
  } else {
    navigation.classList.remove("scrollable");
  }
});

const getActiveNavigation = (btn) => {
  navigationBtns.forEach((navBtn) => {
    navBtn.classList.remove("active");
  });
  btn.classList.add("active");
};

const navigationBtns = navigation.querySelectorAll(".nav-item");

navigationBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault;
    getActiveNavigation(e.target.parentElement);
  });
});
