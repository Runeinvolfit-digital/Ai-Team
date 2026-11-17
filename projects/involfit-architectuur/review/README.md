# Reviewstatus architectuurdemonstratie

**Niet reviewbaar opgeleverd: externe previewlink ontbreekt.**

Gecontroleerd: 2026-11-17T16:15:22+01:00 (Europe/Amsterdam). Bron van de site: `64614ab08e2a6cae193dcba76886f719ae402c4b`, branch `site/involfit-architectuur`. Deze reviewcommit voegt alleen bewijs en documentatie toe; websitecode is ongewijzigd.

[GitHub-projectmap](https://github.com/Runeinvolfit-digital/Ai-Team/tree/site/involfit-architectuur/projects/involfit-architectuur).

## Screenshots van lokale tests

| Pagina | Desktop 1440×1000 | Mobiel 390×844 |
|---|---|---|
| Home | [Screenshot](index-desktop.png) | [Screenshot](index-mobiel.png) |
| Projecten | [Screenshot](projecten-desktop.png) | [Screenshot](projecten-mobiel.png) |
| Contact | [Screenshot](contact-desktop.png) | [Screenshot](contact-mobiel.png) |

Dit zijn volledige paginaopnamen uit Chromium met de bovenstaande viewportafmetingen. Ze komen van een lokale testserver, niet van een extern bereikbare preview. Ze bewijzen dus geen externe bereikbaarheid.

## Werkelijk gecontroleerd

- `python3 tests/browser.py --artifacts /tmp/involfit-review-current`: 11 controlegroepen geslaagd op vier schermformaten; [resultaten](local-test-results.json).
- Apart de server op poort 8000 getest: Home laadt, projectfilter Wonen werkt en lege formulierinvoer toont drie veldfouten.
- De huidige omgevingsstatus meldt uitsluitend een SSH-portal op poort 22 en geen HTTP-preview-URL, ook na starten van de server op 0.0.0.0:8000. Een tool om HTTP-previewtoegang te configureren is hier niet beschikbaar.
- Er is geen externe previewcontrole uitgevoerd. De eerdere uitgebreide tests staan in [TEST-REPORT.md](../TEST-REPORT.md); hun geslaagde status vervangt de previewgate niet.

## Open vereiste

Een ondersteunde HTTP-previewportal voor poort 8000 of een beschikbare testhostingomgeving is nodig. Zodra die een werkelijk adres biedt, moet dat exacte adres in de browser worden gecontroleerd, inclusief de primaire interacties, en moeten bijbehorende screenshots worden vastgelegd. Dan pas kan de status reviewbaar worden.

Er is geen website naar productie gepubliceerd. Definitieve productiepublicatie vereist expliciete goedkeuring van de eigenaar voor de concrete versie en bestemming.
