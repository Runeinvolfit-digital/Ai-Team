# Websitecontrole

De screenshots zijn gemaakt van de lokale productiebuild in Chromium op 17 november 2026, op branch `site/involfit`. Desktop is 1440 × 1000 en mobiel is 390 × 844 CSS-pixels. De afbeeldingen tonen de volledige lengte van de pagina.

| Pagina | Desktop | Mobiel |
| --- | --- | --- |
| Home | [Desktop](home-desktop.png) | [Mobiel](home-mobiel.png) |
| Diensten | [Desktop](diensten-desktop.png) | [Mobiel](diensten-mobiel.png) |
| Contact | [Desktop](contact-desktop.png) | [Mobiel](contact-mobiel.png) |

## Herhalen

Voer vanuit `projects/involfit` de volgende commando’s uit. Voor de browsercontrole zijn Python Playwright en Chromium vereist. Stel zo nodig `CHROMIUM_PATH` in op het geïnstalleerde uitvoerbare bestand.

```bash
npm ci
npm run check
npm test
npm run build
python3 tests/browser.py --screenshots review --results review/test-results.json
```

Voeg `--axe /pad/naar/axe.min.js` toe om de WCAG-regels van axe-core te draaien. De vijf Node-tests gebruiken een echte lokale HTTP-server en een geïnjecteerde mailprovider. De browsertest verifieert ook het formulier zonder mailconfiguratie en controleert of het scherm de werkelijke serverstatus correct weergeeft.

Chromium controleerde alle vier de routes op 360, 390, 768, 1024, 1440 en 1920 px. Alle 24 combinaties slaagden. Tien axe-scans meldden geen overtredingen in de getoetste WCAG-regels. Zie [browserresultaten](test-results.json) voor de geteste interacties en formulierstatussen.

## Lighthouse

Lighthouse 13.6.0 is uitgevoerd op Home, Diensten en Contact, met gesimuleerde mobiele throttling en de lokale server tijdelijk op `SITE_INDEXABLE=1`. Alle drie de pagina’s scoorden 100 op Performance, Accessibility, Best Practices en SEO. De gemeten LCP was 0,90–1,52 seconde, CLS 0,0005–0,0068. Zie [meetgegevens](lighthouse.json). Dit zijn laboratoriummetingen. INP en praktijkmetingen ontbreken.

## Bevindingen en resterende controle

- De Chromium-test vond een door de CSP geblokkeerd inline font. De build serveert fontbestanden nu afzonderlijk. De contactpagina reserveert direct ruimte voor het formulier, waardoor CLS in de lokale Lighthouse-meting daalde van 0,223 tot 0,0005.
- De dependencyvrije HTTP-server heeft geen npm-productiedependencies. De audit van de bouwtools meldde het open picomatch-advies GHSA-fc5q-39xc-vjpf. De registry bood bij controle geen gepatchte versie voor de gemelde reeks. Gebruik alleen vertrouwde bronbestanden in de bouwstap en lever aan de runtime uitsluitend `dist/`, `package.json` en `server.mjs`.
- Er is geen geconfigureerde HTTP-previewportal. De screenshots en metingen zijn lokaal. De vereiste externe preview en live mailbezorging blijven open. Echte mailbezorging vereist een testinbox, een geverifieerde afzender, een Resend-sleutel en toegang tot de Resend-API.
- De publieke inhoudsreferentie was vanuit de cloud geblokkeerd. Voor productie moeten inhoudseigenaar en daadwerkelijke verwerking van persoonsgegevens gecontroleerd worden.
