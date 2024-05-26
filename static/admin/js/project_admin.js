const fileField = document.querySelector("#id_file");
const contentField = document.querySelector("#id_content");
const contentTypes = document.querySelectorAll('input[name="content_type"]');

console.log(contentField, contentField.previousElementSibling);

contentField.previousElementSibling.classList.add("required");
fileField.previousElementSibling.classList.add("required");

function updateFields() {
  const selectedContentType = document.querySelector(
    'input[name="content_type"]:checked'
  ).value;

  if (selectedContentType === "html") {
    fileField.closest(".form-row").classList.add("hidden");
    fileField.removeAttribute("required");
    contentField.closest(".form-row").classList.remove("hidden");
    contentField.setAttribute("required", true);
  } else {
    contentField.closest(".form-row").classList.add("hidden");
    contentField.removeAttribute("required");
    fileField.closest(".form-row").classList.remove("hidden");
    fileField.setAttribute("required", true);
  }
}

document.addEventListener("DOMContentLoaded", updateFields());
contentTypes.forEach((radio) => {
  radio.addEventListener("change", updateFields);
});

// Initialize the fields based on the default selected radio button
updateFields();
