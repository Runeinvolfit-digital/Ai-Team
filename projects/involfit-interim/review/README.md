# Review Involfit B.V. — interimmanagement en organisatieadvies

Gecontroleerd: 2026-11-17T16:42:41+01:00 (Europe/Amsterdam). Websitebron: `b4b6f9af5b1539721940fc135fa96a63dcb5d1e4`, branch `site/involfit-interim`, project `projects/involfit-interim/`.

[Zelfstandige downloadpreview](../index.html) · [GitHub-projectmap](https://github.com/Runeinvolfit-digital/Ai-Team/tree/site/involfit-interim/projects/involfit-interim)

## Inhoud en ontwerp

Gebruikersgegevens: Involfit B.V., Sander de Ridder (oprichter), interimmanagement en organisatieadvies, info@involfit.nl; geen telefoon beschikbaar. Donkerblauw #11263a, wit en zilver #c4ccd3. Ruimte voor een portret, expliciet gemarkeerd met “Portret volgt”. Geen verzonnen foto, klantnamen, resultaten, ervaring, adres of certificeringen. De teksten over de voorgestelde werkwijze zijn conceptcopy voor beoordeling door Sander.

Eén specialist leverde websitecopy en deed een gerichte read-only bronreview; de hoofduitvoerder bouwde en testte. Maximaal twee uitvoerders tegelijk. De review vond dat de hero buiten het main-landmark stond. Dit is gecorrigeerd en de browsertest controleert nu dat de H1 binnen main staat. Geen andere concrete brondefecten gemeld. Geen tokenbesparing gemeten.

## Screenshots

Lokale Chromium-opnamen van dezelfde websiteversie. Dit zijn zichtbare browservensters, geen externe previewcontrole.

| Onderdeel | Desktop 1440×1000 | Mobiel 390×844 |
|---|---|---|
| Introductie en portretvlak | [Screenshot](home-desktop.png) | [Screenshot](home-mobiel.png) |
| Contact | [Screenshot](contact-desktop.png) | [Screenshot](contact-mobiel.png) |

## Werkelijk getest

`python3 tests/browser.py --axe /tmp/involfit-qa/node_modules/axe-core/axe.min.js` — **10 controlegroepen geslaagd**. [Resultaten](test-results.json).

- 1440×1000, 390×844, 320×720, 844×390: geen horizontale overflow; juiste inhoud, werkende ankerdoelen, gereserveerd portretvlak en mailto-adressen.
- axe-core 4.11.0, WCAG2A/AA, WCAG2.1AA en WCAG2.2AA-tags: geen gerapporteerde overtredingen op de vier schermformaten.
- Mobiel menu: openen met Enter, sluiten met Escape, focusherstel, navigeren naar Diensten, sluiten na selectie en focus op de gekozen sectie.
- Navigatie blijft zichtbaar bij overschakelen van mobiel naar desktop.
- Reduced motion schakelt vloeiend scrollen uit.
- Zonder JavaScript blijven navigatie en e-mailcontact beschikbaar.
- Zelfstandige HTML-inhoud met Playwright set_content: menu en inhoud functioneren zonder resourceverzoeken. De download heeft geen externe afhankelijkheden.
- Geen JavaScript- of HTTP-fouten, externe verzoeken, cookies of localStorage/sessionStorage waargenomen.
- `python3 scripts/check-agency.py` vanuit de repositoryroot: 22 rollen en alle 14 kennisbestanden behouden.
- `git diff --check`: geslaagd. Geen build of dependency-installatie nodig.

## Beperkingen en status

**De zelfstandige downloadpreview is beschikbaar; formeel niet reviewbaar opgeleverd volgens de externe-previewgate.** Deze cloudomgeving biedt geen HTTP-previewportal en geen bedienbare zichtbare Codex-browser. Er is geen externe previewlink gecontroleerd. Dit is dezelfde bekende infrastructuurblokkade, geen websitefout.

De exacte zelfstandige documentinhoud is via set_content getest. Direct file:// openen is in de beheerde Chromium-installatie beleidsmatig geblokkeerd; de eigen browserinstellingen van de gebruiker zijn niet getest. Geen screenreaderaudit, fysieke apparaten of Safari/Firefox getest. Een automatische scan is geen WCAG-certificering.

E-mailknoppen bevatten het door de gebruiker opgegeven adres en openen de eigen mailapp. Er is geen formulier of backend; berichten versturen/afleveren is niet uitgevoerd of bewezen. De link “Stuur een e-mail” verzendt op zichzelf niets.

Open: echte portretfoto toevoegen na goedkeuring, conceptcopy laten bevestigen, een externe previewomgeving beschikbaar maken en de exacte preview-URL controleren. Productiepublicatie vereist expliciete toestemming voor versie en bestemming. Er is niets naar productie gepubliceerd. Agency en kennisbank op main en de eerdere architectuurbranch zijn behouden.
