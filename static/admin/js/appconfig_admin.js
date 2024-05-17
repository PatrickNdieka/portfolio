function updateValueField() {
  const valueFields = document.querySelectorAll(
    'input[name$="_value"], textarea[name$="_value"]'
  );
  const valueTypeSelect = document.getElementById("id_value_type");

  valueFields.forEach((field) => {
    field.closest(".form-row").classList.add("hidden");
  });

  const selectedType = valueTypeSelect.value;
  const selectedField = document.getElementById(`id_${selectedType}_value`);
  console.log(valueFields);
  if (selectedField) {
    selectedField.closest(".form-row").classList.remove("hidden");
  }
}

const valueTypeSelect = document.getElementById("id_value_type");
document.addEventListener("DOMContentLoaded", updateValueField);
valueTypeSelect.addEventListener("change", updateValueField);
