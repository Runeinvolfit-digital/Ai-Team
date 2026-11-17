# Review Buitenwerk — hoveniersconcept

Gecontroleerd: 2026-11-17T17:04:13+01:00 (Europe/Amsterdam). Websitebron: `c45980d938ca8a8a3791dfa9d222b74271b2c3fc`, branch `site/buitenwerk-hovenier`. Project: `projects/buitenwerk-hovenier/`.

[Zelfstandige downloadpreview](../index.html) · [GitHub-projectmap](https://github.com/Runeinvolfit-digital/Ai-Team/tree/site/buitenwerk-hovenier/projects/buitenwerk-hovenier)

## Inhoud en ontwerp

De gebruiker koos een hoveniersbedrijf. Naam, werkgebied en contactgegevens ontbreken; “Buitenwerk” is expliciet een werknaam. Geen fictieve klanten, portfolioresultaten, reviews, medewerkers, telefoonnummers, adressen of e-mails toegevoegd. De diensten en aanpak zijn conceptcopy voor latere bevestiging. Het tuinbeeld is voor deze demo AI-gegenereerd en zichtbaar als sfeerbeeld gemarkeerd.

Warm wit, donkergroen en saliegroen. Compacte koppen zonder decoratieve bovenlabels, nummers of pijltjes. De mobiele foto is compact zodat de hoofdkop direct zichtbaar is; in de tuinverkenner staat de bewegende schets direct onder de keuzes en vóór de toelichting. Eén uitvoerder; geen extra agents of tokenbesparingsclaims.

## Eigen functie

De tuinverkenner vertaalt drie wensen naar een schematische tuinindeling en bespreekpunten: meer groen, meer ontspannen, minder onderhoud. Bij een keuze verschuiven en veranderen de plantvakken, het terras en andere illustratieonderdelen. Het is kwalitatieve inspiratie, zonder schaal, maatvoering, technische diagnose, offerte, meetgegevens of resultaatbelofte. Minder onderhoud is nadrukkelijk niet onderhoudsvrij.

“Bewaar mijn tuinidee” maakt lokaal een echt tekstbestand met de gekozen richting, tips en beperkingen. Er is geen formulier, verzending of backend. De download is geen automatisch verzonden aanvraag en schrijft niets naar cookies, localStorage of sessionStorage.

## Screenshots

Lokale Chromium-viewportopnamen van dezelfde bronversie; geen bewijs van externe previewbereikbaarheid.

| Onderdeel | Desktop 1440×1000 | Mobiel 390×844 |
|---|---|---|
| Home | [Screenshot](home-desktop.png) | [Screenshot](home-mobiel.png) |
| Tuinverkenner | [Screenshot](explorer-desktop.png) | [Screenshot](explorer-mobiel.png) |

## Werkelijk uitgevoerd

`python3 tests/browser.py --axe /tmp/involfit-qa/node_modules/axe-core/axe.min.js` — **12 controlegroepen geslaagd**. [Resultaten](test-results.json).

- Vier formaten: 1440×1000, 390×844, 320×720 en 844×390; geen horizontale overflow, beeld geladen, compacte hoofdkop, werkende ankerlinks en duidelijke conceptaanduiding.
- Op smalle schermen is de foto minder dan 300px hoog, staat de hoofdkop binnen het eerste browservenster en staat de schets vóór de dynamische toelichting.
- axe-core 4.11.0 met WCAG2A/AA, WCAG2.1AA en WCAG2.2AA-tags: geen gerapporteerde overtredingen op de vier formaten.
- Mobiel menu met Enter/Escape, focusherstel, werkelijke ankerselectie en sluiten na navigatie.
- Tuinverkenner: selecteren met toetsenbord, aria-pressed, gewijzigd resultaat, actuele SVG-titel en lopende CSS-overgang gecontroleerd.
- Werkelijk tekstbestand gedownload en uitgelezen: gekozen onderhoudsrichting, bestandsnaam en beperkingen kloppen.
- Reduced motion: functie blijft werken zonder plantovergangen en zonder vloeiend scrollen.
- Touch: beide alternatieve keuzes reageren en knophoogte is minimaal 44px.
- Zonder JavaScript blijven navigatie, statisch tuinidee en uitleg beschikbaar; keuzes en download worden niet ten onrechte aangeboden.
- Exacte zelfstandige HTML-inhoud via set_content: foto, keuze en echte download werken zonder HTTP(S)-resourceverzoeken.
- Geen JavaScript-/HTTP-fouten, externe verzoeken, cookies of browseropslag waargenomen.
- Agencychecker: 22 rollen en 14 ongewijzigde kennisbestanden; Git-diff op witruimte gecontroleerd.

De builder berekent CSP-hashes over de exact ingevoegde CSS en JavaScript, inclusief templatewitruimte. Een eerste mismatch is daarmee opgelost; de beveiliging is niet versoepeld. Het bouwen wordt gecontroleerd op een identiek resultaat bij ongewijzigde bronbestanden.

## Status en open punten

**Downloadbare conceptpreview beschikbaar; formeel niet reviewbaar opgeleverd volgens de externe-previewgate.** De bekende Codex-omgeving biedt nog geen bruikbare externe HTTP-previewlink of bedienbare zichtbare browser. Er is geen externe previewcontrole uitgevoerd en niets naar productie gepubliceerd.

De zelfstandige HTML-inhoud is via set_content getest. Direct openen via file:// is in de beheerde Chromium-installatie beleidsmatig geblokkeerd; dit beleid is niet uitgezet. De lokale browser van de gebruiker is niet getest. Geen volledige screenreader-/WCAG-audit, fysieke apparaten, Safari of Firefox getest. Geen professionele tuinbouwkundige of bouwkundige validatie van de schetsen uitgevoerd.

Nog nodig voor een echte bedrijfssite: bedrijfsnaam, diensten en werkgebied bevestigen; echte contactgegevens en eventueel eigen foto's toevoegen; echte externe preview controleren. Productiepublicatie vereist expliciete eigenaarstoestemming voor versie en bestemming. De agency/kennisbank blijven op main; eerdere websites zijn niet gewijzigd.
