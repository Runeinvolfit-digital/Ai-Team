# Buitenwerk — websiteconcept voor een hoveniersbedrijf

Een concept voor tuinaanleg en tuinonderhoud. “Buitenwerk” is een fictieve werknaam: de gebruiker gaf nog geen bedrijfsnaam of contactgegevens. Er zijn geen klantprojecten, contactgegevens, testimonials, teamleden, ervaringsjaren of bedrijfsresultaten verzonnen. Het tuinbeeld is voor deze demo met OpenAI image generation gemaakt en zichtbaar als AI-sfeerbeeld gemarkeerd.

## Bekijken

`index.html` is een zelfstandige downloadpreview: CSS, JavaScript, foto en SVG zijn ingebed. Download en open het bestand in een browser. Er zijn geen externe fonts, CDN's, runtime-dependencies of backend. Een klik op “Bewaar mijn tuinidee” biedt lokaal een tekstbestand aan; er wordt niets verzonden of in cookies/browseropslag bewaard.

Ontwikkelserver: `python3 -m http.server 3002 --bind 0.0.0.0` vanuit deze map. Dit lokale adres is geen gecontroleerde externe previewlink. De bekende Codex-omgeving biedt geen bruikbare HTTP-previewportal of bedienbare zichtbare browser; de downloadpreview is het beschikbare alternatief.

## Bewerken en bouwen

Bewerk `src/page.html`, `src/styles.css` en `src/app.js`. De foto staat in `assets/garden.webp`. Bouw daarna met `python3 tools/build.py` (alleen Python-standaardbibliotheek). De builder berekent CSP-hashes over de exact ingebedde tekst; script/style-beveiliging wordt niet uitgezet.

De tuinverkenner heeft drie keuzes: meer groen, meer ontspannen en minder onderhoud. De SVG-tuin verandert met een korte overgang en de tekst geeft bespreekpunten. Het is schematische inspiratie zonder schaal, plantlocatieadvies, kostenberekening of resultaatbelofte. Bodem, ligging, budget en zorg moeten met een echte hovenier worden besproken. “Minder onderhoud” betekent niet onderhoudsvrij.

De functie ondersteunt toetsenbord en touch. Beweging vervalt bij prefers-reduced-motion. Zonder JavaScript blijven de kerninhoud en een statische uitleg zichtbaar; de interactieve keuzes en download zijn dan eerlijk uitgeschakeld.

## Tests

`python3 tests/browser.py` vereist bestaande Python Playwright en `/usr/bin/chromium`. Optioneel `--axe /pad/naar/axe.min.js` voor geautomatiseerde toegankelijkheidscontrole. De runner start en stopt zijn eigen lokale server. Resultaten en screenshots gaan naar `/tmp/buitenwerk-review/`. Zie `review/README.md` voor uitgevoerde controles, screenshotlinks en beperkingen.

## Branch en opleverstatus

`site/buitenwerk-hovenier`, gebaseerd op `main`, bestanden in `projects/buitenwerk-hovenier/`. De agency en kennisbank blijven op main en andere websites blijven op hun eigen branches.

Zonder een gecontroleerde externe previewlink is dit volgens de agency-previewgate nog niet formeel reviewbaar opgeleverd. Geen productiepublicatie uitgevoerd; daarvoor is expliciete eigenaarstoestemming nodig. Vóór productie moeten echte naam, diensten, werkgebied en contactgegevens worden bevestigd, echte fotografie zo nodig worden toegevoegd en noindex/metadata worden beoordeeld.
