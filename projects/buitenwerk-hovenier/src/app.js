const header = document.querySelector(".site-header");
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("#navigation");
function closeMenu() {
  toggle.setAttribute("aria-expanded", "false");
  nav.classList.remove("is-open");
}
header.classList.add("enhanced");
toggle.hidden = false;
toggle.addEventListener("click", () => {
  const open = toggle.getAttribute("aria-expanded") !== "true";
  toggle.setAttribute("aria-expanded", String(open));
  nav.classList.toggle("is-open", open);
});
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    toggle.getAttribute("aria-expanded") === "true"
  ) {
    closeMenu();
    toggle.focus();
  }
});
nav.addEventListener("click", (event) => {
  const link = event.target.closest('a[href^="#"]');
  if (link) {
    closeMenu();
    document
      .querySelector(link.getAttribute("href"))
      ?.focus({ preventScroll: true });
  }
});
const ideas = {
  groen: {
    title: "Een tuin die leeft",
    description:
      "Meer ruimte voor gelaagde beplanting, bloemen en een groene rand. Een uitnodiging om groen de hoofdrol te geven.",
    tips: [
      "Bespreek waar bomen, heesters en borders passen.",
      "Laat bodem, zon en schaduw de plantkeuze bepalen.",
      "Houd ruimte voor een prettig pad en een zitplek.",
    ],
  },
  rust: {
    title: "Een plek om te blijven",
    description:
      "Een ruimere zitplek, een beschutte hoek en groen dat rust brengt. Buiten als verlengstuk van het huis.",
    tips: [
      "Bepaal wanneer u graag buiten zit.",
      "Denk aan schaduw, zichtlijnen en beschutting.",
      "Breng terras en beplanting met elkaar in balans.",
    ],
  },
  gemak: {
    title: "Overzichtelijk en groen",
    description:
      "Een heldere indeling en samenhangende plantvakken kunnen het onderhoud beter planbaar maken. Onderhoudsvrij wordt een tuin nooit.",
    tips: [
      "Bespreek hoeveel tijd u aan onderhoud wilt besteden.",
      "Kies beplanting die bij de plek en beschikbare zorg past.",
      "Maak paden en plantvakken goed bereikbaar.",
    ],
  },
};
let selected = "groen";
const controls = document.querySelector(".garden-choices");
const scene = document.querySelector(".garden-scene");
const status = document.querySelector("#idea-status");
const saveButton = document.querySelector("#save-idea");
controls.hidden = false;
saveButton.disabled = false;
controls.querySelectorAll("[data-choice]").forEach((button) =>
  button.addEventListener("click", () => {
    const key = button.dataset.choice;
    if (key === selected) return;
    selected = key;
    const idea = ideas[key];
    scene.dataset.garden = key;
    controls
      .querySelectorAll("[data-choice]")
      .forEach((option) =>
        option.setAttribute("aria-pressed", String(option === button)),
      );
    document.querySelector("#idea-title").textContent = idea.title;
    document.querySelector("#idea-description").textContent = idea.description;
    const list = document.querySelector("#idea-tips");
    list.replaceChildren(
      ...idea.tips.map((text) => {
        const li = document.createElement("li");
        li.textContent = text;
        return li;
      }),
    );
    document.querySelector("#garden-title").textContent =
      "Schematische tuin: " + idea.title;
    document.querySelector("#garden-description").textContent =
      idea.description +
      " Illustratie zonder schaal of afmetingen, geen uitgewerkt tuinontwerp.";
    status.textContent = "";
  }),
);
saveButton.addEventListener("click", () => {
  const idea = ideas[selected];
  const content =
    "MIJN TUINIDEE\n\n" +
    idea.title +
    "\n" +
    idea.description +
    "\n\nAandachtspunten\n" +
    idea.tips.map((t) => "• " + t).join("\n") +
    "\n\nConceptinspiratie van Buitenwerk (werknaam). Geen offerte, beplantingsadvies op maat of ontwerp op schaal. Bespreek bodem, ligging, afmetingen en budget met een hovenier. Er is niets verstuurd.\n";
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "mijn-tuinidee-" + selected + ".txt";
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status.textContent =
    "Uw tuinidee is als tekstbestand aangeboden. Er is niets verstuurd of op de website opgeslagen.";
});
