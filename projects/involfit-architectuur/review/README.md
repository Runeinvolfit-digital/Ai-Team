# Reviewstatus architectuurdemonstratie

**Niet reviewbaar opgeleverd: externe previewlink ontbreekt.**

Gecontroleerd: 2026-11-17T16:17:33+01:00 (Europe/Amsterdam). Bron van de site: `64614ab08e2a6cae193dcba76886f719ae402c4b`, branch `site/involfit-architectuur`. De reviewcommits voegen bewijs, documentatie en een betrouwbaardere screenshotprocedure toe; de websitecode is ongewijzigd.

[GitHub-projectmap](https://github.com/Runeinvolfit-digital/Ai-Team/tree/site/involfit-architectuur/projects/involfit-architectuur).

## Screenshots van lokale tests

| Pagina | Desktop 1440×1000 | Mobiel 390×844 |
|---|---|---|
| Home | [Screenshot](index-desktop.png) | [Screenshot](index-mobiel.png) |
| Projecten | [Screenshot](projecten-desktop.png) | [Screenshot](projecten-mobiel.png) |
| Contact | [Screenshot](contact-desktop.png) | [Screenshot](contact-mobiel.png) |

Dit zijn opnamen van het zichtbare browservenster uit Chromium met de bovenstaande viewportafmetingen. Volledige paginaopnamen gaven in deze runtime incidentele renderartefacten; de testrunner legt daarom het geteste browservenster vast na het laden/decoderen van de afbeeldingen. Ze komen van een lokale testserver, niet van een extern bereikbare preview. Ze bewijzen dus geen externe bereikbaarheid.

## Werkelijk gecontroleerd

- `python3 tests/browser.py --artifacts /tmp/involfit-review-viewport`: 11 controlegroepen geslaagd op vier schermformaten; [resultaten](local-test-results.json).
- Apart de server op poort 8000 getest: Home laadt, projectfilter Wonen werkt en lege formulierinvoer toont drie veldfouten.
- De huidige omgevingsstatus meldt uitsluitend een SSH-portal op poort 22 en geen HTTP-preview-URL, ook na starten van de server op 0.0.0.0:8000. Een tool om HTTP-previewtoegang te configureren is hier niet beschikbaar.
- Er is geen externe previewcontrole uitgevoerd. De eerdere uitgebreide tests staan in [TEST-REPORT.md](../TEST-REPORT.md); hun geslaagde status vervangt de previewgate niet.

## Open vereiste

Een ondersteunde HTTP-previewportal voor poort 8000 of een beschikbare testhostingomgeving is nodig. Zodra die een werkelijk adres biedt, moet dat exacte adres in de browser worden gecontroleerd, inclusief de primaire interacties, en moeten bijbehorende screenshots worden vastgelegd. Dan pas kan de status reviewbaar worden.

Er is geen website naar productie gepubliceerd. Definitieve productiepublicatie vereist expliciete goedkeuring van de eigenaar voor de concrete versie en bestemming.

## Downloadbare offline preview

[Download het zelfstandige HTML-bestand](involfit-preview.html). Sla het op en open het op je eigen computer in een browser; CSS, scripts en afbeeldingen zijn ingebed. Navigatie tussen Home, Projecten en Contact gebeurt binnen het bestand. Geen installatie, webserver, externe afbeeldingsdienst of backend nodig.

Reproduceren vanuit de projectmap: `python3 tools/export-preview.py`. Controleren: `python3 tests/offline-preview.py`. De export heeft een eigen CSP met hashes voor de ingebedde scripts/styles; de CSP en code van de gewone website blijven ongewijzigd.

Werkelijk getest: de exacte HTML-inhoud via Playwright `set_content`, op 1440×1000 en 390×844. Navigatie, afbeeldingen, projectfilters, ongeldige/geldige formulierinvoer en geen externe HTTP(S)-verzoeken of JavaScriptfouten: geslaagd. Direct openen als `file://` is in deze beheerde Chromium-installatie geblokkeerd met `ERR_BLOCKED_BY_ADMINISTRATOR`; dit beleid is niet uitgezet. De lokale browserinstellingen van de gebruiker zijn niet getest.

Dit is een downloadbare lokale preview. De eerder gemelde blokkade voor een gehoste previewlink blijft bestaan; er is niets naar productie gepubliceerd.
