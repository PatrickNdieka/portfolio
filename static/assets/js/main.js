// Helper Function to modify the path by replacing the last variable of theme file
function modifyPath(path, newVariable) {
  const parts = path.split("/");
  parts[parts.length - 1] = newVariable;
  return parts.join("/");
}

// Function to change the Webpage theme
function changeTheme(currentTheme) {
  setCookie("theme_mode", currentTheme);
  const notebookLink = document.getElementById("notebook_styles_variables");
  // Change the theme cookie appropriately to current theme
  document.documentElement.setAttribute(
    "data-theme-light",
    `${"light" === currentTheme}`
  );
  if (notebookLink) {
    const originPath = notebookLink.href;
    notebookLink.href = modifyPath(
      originPath,
      `notebook_${currentTheme}_mode.css`
    );
    const bodyElement = document.querySelector("body");
    bodyElement.setAttribute(
      "data-jp-theme-light",
      `${"light" === currentTheme}`
    );
    bodyElement.setAttribute("jp-theme-name", `JupyterLab ${currentTheme}`);
  }
}

// Funstion to change the correct active navigation button
function getActiveNavigation(btn) {
  navigationBtns.forEach((navBtn) => {
    navBtn.classList.remove("active");
  });
  btn.classList.add("active");
}

// Function to check for consent and show consent form
function checkConsentAndFetchMessage() {
  const consentGivenCookie = getCookie("consent_given") ? true : false;
  const consentRejectedCookie = getCookie("consent_rejected") ? true : false;
  console.log(consentGivenCookie, consentRejectedCookie);
  if (!consentGivenCookie && !consentRejectedCookie) {
    console.log("Fetching consent message");
    fetchConsentMessage();
    console.log("Fetched consent message");
  } else {
    removeConsentPopup();
  }
}

function fetchConsentMessage() {
  const container = document.getElementById("consent-message-popup");
  const url = container.getAttribute("data-url");
  // issue a GET to url and replace #consent-message-popup with the response
  htmx.ajax("GET", url, {
    target: "#consent-message-popup",
    swap: "outerHTML",
  });
}

// Helper function to reject the consent for cookie setting
function giveConsent() {
  setCookie("consent_given", "true", 365); // Set a cookie named 'consent_given' with an expiry date of 1 year from now
  removeConsentPopup();
}

// Helper function to reject the consent for cookie setting
function rejectConsent() {
  setCookie("consent_rejected", "true"); // Set a session cookie
  removeConsentPopup();
}

// Function to remove the consent form
function removeConsentPopup() {
  // Remove the consent popup from the DOM
  const consentPopup = document.getElementById("consent-message-popup");
  consentPopup.parentNode.removeChild(consentPopup);
}

// Function to set a cookie
function setCookie(
  cookieName,
  cookieValue,
  expireDays = 0,
  httpOnly = false,
  sameSite = "Lax"
) {
  const encodedCookieName = encodeURIComponent(cookieName);
  const encodedCookieValue = encodeURIComponent(cookieValue);

  let cookieString = `${encodedCookieName}=${encodedCookieValue}`;
  if (expireDays > 0) {
    const expirationDate = new Date();
    expirationDate.setTime(
      expirationDate.getTime() + expireDays * 24 * 60 * 60 * 1000
    );
    cookieString += `; expires=${expirationDate.toUTCString()}`;
  }
  cookieString += "; path=/";

  if (httpOnly) {
    cookieString += "; HttpOnly"; // Add HttpOnly attribute if true
  }

  cookieString += `; SameSite=${sameSite}`; // Add SameSite attribute

  const domain = getDomainForCookie();
  if (domain) {
    cookieString += `; Domain=${domain}`;
  }

  document.cookie = cookieString; // Set the cookie
}

// Function to get a given cookie
function getCookie(cookieName) {
  const encodedCookieName = encodeURIComponent(cookieName);
  const cookies = document.cookie.split(";");

  // Loop through each cookie
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i];
    cookie = cookie.trim();
    if (cookie.startsWith(encodedCookieName + "=")) {
      if (navigator.cookieEnabled && !isCookieSameSitePermitted(cookie)) {
        return null; // Don't access cookie if SameSite prevents it
      }
      return cookie.split("=")[1];
    }
  }
  return null;
}

// Helper function to check if cookie SameSite attribute allows access
function isCookieSameSitePermitted(cookieString) {
  const sameSiteAttr = cookieString
    .split(";")
    .find((part) => part.trim().startsWith("SameSite="));
  if (!sameSiteAttr) {
    return true; // No SameSite attribute, likely pre-standard cookie, so assume Lax for compatibility
  }
  const sameSiteValue = sameSiteAttr.split("=")[1];
  return (
    sameSiteValue === "Lax" ||
    document.location.hostname === getCookieDomain(cookieString)
  ); // Allow access for Lax within same site and Strict for same domain
}

// Helper function to extract cookie domain (currently not used)
function getCookieDomain(cookieString) {
  const domainAttr = cookieString
    .split(";")
    .find((part) => part.trim().startsWith("Domain="));
  return domainAttr ? domainAttr.split("=")[1] : null;
}

// Helper function to get the domain for the cookie
function getDomainForCookie() {
  return document.location.hostname; // Return the current hostname
}

// function to clear the newsletter inputs
function clearNewsletterForm() {
  const subscriberInputs = document.querySelectorAll(".newsletter-form input");
  subscriberInputs.forEach((input) => {
    input.value = "";
  });
}

// function to show/hide the modal on htmx requests
function showModalOnHtmx() {
  // Add event listener to close button
  document.querySelector("#modal .close").addEventListener("click", () => {
    document.getElementById("modal").classList.remove("show");
    document.getElementById("modal").firstElementChild.remove();
  });
  document.getElementById("modal").classList.add("show");
}

const menuToggleBtn = document.querySelector(".menu-toggle");
const navMenu = document.querySelector("#nav-menu");
const navigation = document.querySelector(".nav");
const navigationBtns = navigation.querySelectorAll(".nav-item");
const prefersDarkTheme = window.matchMedia("(prefers-color-scheme: dark)"); // Check the initial preference
const newTheme = prefersDarkTheme.matches ? "dark" : "light";
const themeCookie = getCookie("theme_mode");
const themeToggleBtn = document.querySelector(".theme-toggle");

window.addEventListener("DOMContentLoaded", function () {
  // change to the correct theme according to the stored cookie or browser preference
  if (themeCookie) {
    changeTheme(themeCookie);
  } else {
    changeTheme(newTheme);
  }
  // Add scrolling effect on the navigation
  if (navigation.getBoundingClientRect().top == 0) {
    navigation.classList.add("scrollable");
  } else {
    navigation.classList.remove("scrollable");
  }
  // EventListeners
  // Show / hide the menu navigation when hidden functionality
  menuToggleBtn.addEventListener("click", () => {
    navMenu.classList.toggle("show");
  });

  // add crolling effect on the right section of the homepage
  navigationBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault;
      getActiveNavigation(e.target.parentElement);
    });
  });

  // Listen for preference changes
  prefersDarkTheme.addEventListener("change", (event) => {
    newTheme = event.matches ? "dark" : "light";
    changeTheme(newTheme); // Update your website's theme based on the new preference
  });
  // Add event listener for the theme button change
  themeToggleBtn.addEventListener("click", (e) => {
    const theme = getCookie("theme_mode") === "dark" ? "light" : "dark"; // check what the current theme is by checking the theme cookie
    changeTheme(theme); // Update your website's theme based on the new preference
  });
  // Check for consent and fetch consent message appropriately
  checkConsentAndFetchMessage();
});

window.addEventListener("scroll", () => {
  if (navigation.getBoundingClientRect().top == 0) {
    navigation.classList.add("scrollable");
  } else {
    navigation.classList.remove("scrollable");
  }
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
