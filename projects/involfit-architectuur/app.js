import { validateContact } from "./validation.mjs";

const toggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#navigation");
if (toggle && navigation) {
  document.querySelector(".site-header").classList.add("has-menu");
  toggle.hidden = false;
  const close = () => {
    toggle.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
  };
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("is-open", open);
  });
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      toggle.getAttribute("aria-expanded") === "true"
    ) {
      close();
      toggle.focus();
    }
  });
  navigation.addEventListener("click", close);
}

const filters = document.querySelectorAll("[data-filter]");
if (filters.length) {
  document.querySelector(".filter-bar").hidden = false;
  filters.forEach((button) =>
    button.addEventListener("click", () => {
      let visible = 0;
      filters.forEach((filter) =>
        filter.setAttribute("aria-pressed", String(filter === button)),
      );
      document.querySelectorAll("[data-category]").forEach((project) => {
        project.hidden =
          button.dataset.filter !== "all" &&
          project.dataset.category !== button.dataset.filter;
        if (!project.hidden) visible += 1;
      });
      document.querySelector("#filter-status").textContent =
        `${visible} ${visible === 1 ? "fictief project" : "fictieve projecten"}`;
    }),
  );
}

const form = document.querySelector("#contact-form");
if (form) {
  const status = document.querySelector("#form-status");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const errors = validateContact(Object.fromEntries(new FormData(form)));
    for (const id of ["name", "email", "message"]) {
      const field = form.elements.namedItem(id);
      field.setAttribute("aria-invalid", String(Boolean(errors[id])));
      document.getElementById(`${id}-error`).textContent = errors[id] || "";
    }
    const firstInvalid = Object.keys(errors)[0];
    if (firstInvalid) {
      status.textContent =
        "Controleer de gemarkeerde velden. Er is niets verstuurd.";
      form.elements.namedItem(firstInvalid).focus();
      return;
    }
    status.textContent =
      "Uw demo-invoer is geldig. Er is niets verstuurd of opgeslagen. Deze website heeft geen backend of contactdienst.";
    status.focus();
  });
  form.addEventListener("input", (event) => {
    status.textContent = "";
    if (event.target.getAttribute("aria-invalid") === "true") {
      event.target.removeAttribute("aria-invalid");
      document.getElementById(`${event.target.id}-error`).textContent = "";
    }
  });
  form.querySelector('[type="submit"]').disabled = false;
}
