# Involfit B.V. — interimmanagement en organisatieadvies

Onepager voor Sander de Ridder, oprichter van Involfit B.V. Donkerblauw, wit en zilver. Diensten, werkwijze, over Sander en contact. Werkelijk opgegeven e-mailadres: info@involfit.nl. Geen telefoonnummer, klantnamen, ervaring of resultaten verzonnen. Er is ruimte gereserveerd voor een portret; er wordt geen fictieve foto van Sander getoond.

## Bekijken

`index.html` is de volledige website: CSS, menu-JavaScript en vectoricoontjes zijn ingebed. Download en open het bestand in je browser. Er zijn geen externe fonts, afbeeldingen, dependencies, cookies, tracking of formulierbackend. E-mailknoppen gebruiken `mailto:` en openen de eigen mailapp; aflevering van berichten is niet getest.

Voor de lokale ontwikkelserver: `python3 -m http.server 3001 --bind 0.0.0.0` vanuit deze map. Een localhost-adres is geen bevestigde externe previewlink. De huidige cloudomgeving biedt nog geen HTTP-previewportal of bedienbare zichtbare Codex-browser. De zelfstandige download is het beschikbare alternatief; volgens de agency-previewgate is er zonder een gecontroleerde externe previewlink nog geen formeel reviewbare oplevering.

## Portret toevoegen

Vervang de inhoud van `.portrait-space` door een echte, goedgekeurde foto met een passende alt-tekst. Gebruik alleen een foto met toestemming van Sander. Pas zo nodig de CSP aan voor een lokale afbeelding (`img-src 'self' data:`); voor een zelfstandige download kan de foto als data-URI worden ingebed. Verwijder dan de tekst “Portret volgt” en de gereserveerde-ruimteomschrijving. De secties en mobiele leesvolgorde blijven behouden.

## Wijzigen en controleren

Bewerk de inline stijl en het script in index.html. De CSP gebruikt SHA-256-hashes; voer na wijzigingen `python3 tools/refresh-csp.py` uit. Alle documenten en scripts blijven binnen dit project.

Tests: `python3 tests/browser.py`; optioneel met `--axe /pad/naar/axe.min.js` voor automatische toegankelijkheidsscans. De tests gebruiken een eigen tijdelijke server en bestaande Python Playwright/Chromium. Geen bouwstap nodig. Zie review/README.md voor werkelijk uitgevoerde tests, screenshots en beperkingen.

## Branch

`site/involfit-interim`, gebaseerd op `main`; projectmap `projects/involfit-interim/`. Agency en kennisbank blijven op `main`. Geen website naar productie publiceren zonder expliciete goedkeuring. De preview heeft bewust noindex/nofollow; controleer metadata en bedrijfsinhoud vóór een eventuele goedgekeurde productiepublicatie.
