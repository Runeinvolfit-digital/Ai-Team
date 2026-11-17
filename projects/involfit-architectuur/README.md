# Involfit B.V. — architectuurdemonstratie

Drie statische pagina's: [Home](index.html), [Projecten](projecten.html), [Contact](contact.html). Projecten en AI-gegenereerde beelden zijn fictief. Geen werkelijke architectuurclaims, adressen of klantcases. Het formulier controleert alleen lokaal: geen backend, verzending, tracking, cookies of opslag. Gebruik fictieve testgegevens.

## Lokaal starten

Vanuit deze map: `python3 -m http.server 8000 --bind 0.0.0.0`.
Open de lokale server in een browser. Geen build, bundler, runtime-dependencies of secrets nodig. Gebruik HTTP: JavaScriptmodules werken niet betrouwbaar onder file://.

## Tests

- `node --test tests/validation.test.mjs` — zeven tests voor verplichte velden, grenswaarden, e-mailadressen en neveneffecten.
- `python3 tests/browser.py` — echte Chromium-controles op 1440×1000, 390×844, 320×720 en 844×390, navigatie, filters, formulier, geen externe verzoeken/opslag en JavaScript-uitval.
- Browsertest vereist Python-package `playwright` en `/usr/bin/chromium`; deze zijn in de voorbereide cloudomgeving aanwezig. De test start en stopt zijn eigen tijdelijke server.
- Optionele automatische toegankelijkheidsscan: `python3 tests/browser.py --axe /pad/naar/axe.min.js`. Bij deze oplevering is axe-core 4.11.0 buiten de checkout geïnstalleerd via npm. Dit is geen claim van volledige WCAG-conformiteit.
- Screenshots en resultaten gaan standaard naar `/tmp/involfit-browser/`, niet naar Git.
- Vanuit de repositoryroot: `python3 scripts/check-agency.py` en `git diff --check`.

## Ontwerp en assets

Ivoor #f3efe7, espresso #302a24, koper #8a452c. Systeemlettertypen Georgia en Arial; geen externe fonts of afbeeldingsdiensten. De originele conceptbeelden zijn met OpenAI image generation voor deze demo gemaakt. Lokale WebP-varianten (720/1600px) beperken dataverkeer; de SVG-favicon is eigen werk. Beelden zijn sfeerillustraties, geen bouwkundige tekeningen of bestaande panden.

## Branchbeleid

Deze website staat uitsluitend op `site/involfit-architectuur`, gebaseerd op `main`, in `projects/involfit-architectuur/`. De gedeelde agencyconfiguratie en kennisbank blijven op `main`. Geen GitHub Pages, hosting of productiepublicatie ingesteld. De demo heeft `noindex, nofollow`; CSP blokkeert connecties en formulierverzending. Een eventuele latere publicatie vraagt een aparte opdracht en controle van echte bedrijfsinformatie en serverheaders.

## Huidige reviewstatus

[Reviewbewijs en screenshots](review/README.md). Volgens de aangescherpte oplevervoorwaarde is de site nog niet reviewbaar opgeleverd zolang een gecontroleerde externe previewlink ontbreekt. Lokale tests en screenshots vervangen die link niet.

## Preview zonder server

[Zelfstandige downloadpreview](review/involfit-preview.html): één HTML-bestand met alle drie pagina's en ingebedde assets. Zie [testmethode en beperkingen](review/README.md#downloadbare-offline-preview). Genereren: `python3 tools/export-preview.py`; documenttest: `python3 tests/offline-preview.py`.
