const operationSelect = document.getElementById("operation");
const equationNode = document.getElementById("equation");
const fieldsNode = document.getElementById("fields");
const resultNode = document.getElementById("result");
const form = document.getElementById("calc-form");

let operations = {};

function createField(key, label) {
  const wrapper = document.createElement("div");
  const labelEl = document.createElement("label");
  const input = document.createElement("input");

  labelEl.textContent = label;
  labelEl.htmlFor = key;

  input.id = key;
  input.name = key;
  input.type = "number";
  input.step = "any";
  input.required = true;

  wrapper.appendChild(labelEl);
  wrapper.appendChild(input);
  return wrapper;
}

function setResult(message, isError = false) {
  resultNode.textContent = message;
  resultNode.classList.toggle("error", isError);
}

function renderFields(operationKey) {
  const operation = operations[operationKey];
  if (!operation) {
    setResult("Selected calculator is unavailable.", true);
    equationNode.textContent = "";
    fieldsNode.innerHTML = "";
    return;
  }

  equationNode.textContent = `Equation: ${operation.equation}`;
  fieldsNode.innerHTML = "";

  Object.entries(operation.variables).forEach(([key, label]) => {
    fieldsNode.appendChild(createField(key, label));
  });
}

async function loadOperations() {
  const response = await fetch("/api");
  if (!response.ok) {
    throw new Error("Unable to read API metadata");
  }

  const payload = await response.json();
  operations = payload.operations || {};

  operationSelect.innerHTML = "";
  Object.entries(operations).forEach(([key, operation]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = operation.name;
    operationSelect.appendChild(option);
  });

  const firstKey = Object.keys(operations)[0];
  if (!firstKey) {
    throw new Error("No calculators available");
  }

  operationSelect.value = firstKey;
  renderFields(firstKey);
}

operationSelect.addEventListener("change", () => renderFields(operationSelect.value));

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form).entries());

  const response = await fetch(`/api/${operationSelect.value}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const payload = await response.json();

  if (!response.ok) {
    setResult(payload.error || "Request failed", true);
    return;
  }

  setResult(`${payload.name}: ${payload.result.toFixed(6)}`);
});

loadOperations().catch((error) => setResult(error.message || "Could not load API metadata", true));
