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

const navigationBtns = navigation.querySelectorAll(".nav-item");

const getActiveNavigation = (btn) => {
  navigationBtns.forEach((navBtn) => {
    navBtn.classList.remove("active");
  });
  btn.classList.add("active");
};

navigationBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault;
    getActiveNavigation(e.target.parentElement);
  });
});

function checkConsentAndFetchMessage() {
  var consentGivenCookie = getCookie("consent_given");
  var consentRejectedCookie = getCookie("consent_rejected");

  if (!consentGivenCookie && !consentRejectedCookie) {
    fetchConsentMessage();
  } else {
    removeConsentPopup();
  }
}

function fetchConsentMessage() {
  var container = document.getElementById("consent-message-popup");
  var url = container.getAttribute("data-url");
  // issue a GET to url and replace #consent-message-popup with the response
  htmx.ajax("GET", url, {
    target: "#consent-message-popup",
    swap: "outerHTML",
  });
}

function giveConsent() {
  // Set a cookie named 'consent_given' with an expiry date
  var expiryDate = new Date();
  expiryDate.setFullYear(expiryDate.getFullYear() + 1); // Expiry date set to one year from now
  document.cookie =
    "consent_given=true; expires=" + expiryDate.toUTCString() + "; path=/";

  removeConsentPopup();
}

function rejectConsent() {
  // Set a session cookie
  document.cookie = "consent_rejected=true";
  removeConsentPopup();
}

function removeConsentPopup() {
  // Remove the consent popup from the DOM
  var consentPopup = document.getElementById("consent-message-popup");
  consentPopup.parentNode.removeChild(consentPopup);
}

function getCookie(cookieName) {
  var name = cookieName + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(";");
  for (var i = 0; i < cookieArray.length; i++) {
    var cookie = cookieArray[i];
    while (cookie.charAt(0) == " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) == 0) {
      return true; // Cookie exists
    }
  }
  return false; // Cookie does not exist
}

document.addEventListener("DOMContentLoaded", function () {
  checkConsentAndFetchMessage();
});

document.addEventListener("htmx:afterSwap", (event) => {
  // Check if the swapped content is the modal content
  if (event.detail.target.id === "modal") {
    clearNewsletterForm();
    showModalOnHtmx();
  }
});

document.body.addEventListener("htmx:afterRequest", function (event) {
  if (event.detail.xhr.status === 400 && event.detail.target.id === "modal") {
    const errorHtml = event.detail.xhr.response;
    modal = document.getElementById("modal");
    modal.innerHTML = errorHtml;
    clearNewsletterForm();
    showModalOnHtmx();
  }
});

function clearNewsletterForm() {
  const subscriberInputs = document.querySelectorAll(".newsletter-form input");
  subscriberInputs.forEach((input) => {
    input.value = "";
  });
}

function showModalOnHtmx() {
  // Add event listener to close button
  document.querySelector("#modal .close").addEventListener("click", () => {
    document.getElementById("modal").classList.remove("show");
    document.getElementById("modal").firstElementChild.remove();
  });
  htmx.addClass(document.getElementById("modal"), "show");
}
