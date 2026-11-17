# Verificatie — 17 november 2026

Scope: statische architectuurdemonstratie op branch `site/involfit-architectuur`, map `projects/involfit-architectuur/`. Agency en kennisbank blijven op `main`. Geen productiepublicatie.

| Controle | Uitgevoerd | Resultaat |
|---|---|---|
| GitHub schrijven | Echte commits en pushes; remote ref vergeleken met lokale SHA | Geslaagd voor agency op main en website op sitebranch |
| Agencyconfiguratie | `python3 scripts/check-agency.py` | 22 rollen, vier leads, zeventien specialisten, vier skills, vier templates |
| Behoud kennisbank | SHA-baseline en Git-diff tegen oorspronkelijke commit | Alle 14 kennisbestanden behouden |
| Formuliervalidatie | `node --test tests/validation.test.mjs` | 7 geslaagd; 0 mislukt of overgeslagen |
| Browserfunctionele checks | `python3 tests/browser.py --axe /tmp/involfit-qa/node_modules/axe-core/axe.min.js` | 11 controlegroepen geslaagd |
| Responsiviteit | Alle drie pagina's op 1440×1000, 390×844, 320×720 en 844×390 | Geen horizontale overflow; afbeeldingen laden; actieve navigatie klopt |
| Toegankelijkheid automatisch | axe-core 4.11.0, WCAG2A/AA, WCAG2.1AA en WCAG2.2AA-tags, 12 pagina/formaat-combinaties | Geen gerapporteerde overtredingen na correctie |
| Toetsenbord | Menu openen met Enter, sluiten met Escape, focusherstel, navigatie | Geslaagd |
| Projecten | Wonen/Cultuur/Alle-projecten-filters, live telling, uitklapbare toelichting | Geslaagd |
| Contact | Verplichte velden, ongeldige/geldige invoer, fouten en focus, drie select-opties | Geslaagd |
| Datagedrag | Verzoeken tijdens formulierinteractie, cookies, localStorage en sessionStorage | Geen verzending of opslag waargenomen |
| HTML-invoer | HTML-achtige naam in formulier | Niet als HTML geïnterpreteerd |
| JavaScript uit | Navigatie en beide projecten zichtbaar; formulierknop uitgeschakeld | Geslaagd |
| Reduced motion | Browser emuleert voorkeur voor minder beweging | Automatisch scrollen uit |
| Runtime | JavaScript-fouten, HTTP-fouten, externe verzoeken | Geen waargenomen |
| Visuele controle | Desktop- en mobiele Home-screenshots bekeken | Illustraties, typografie en SVG-iconen gecontroleerd |
| Bronopmaak | Prettier 3.6.2 check op HTML, CSS, JS en MJS; `git diff --check` | Geslaagd |
| Onafhankelijke review | Aparte read-only reviewsessie; 7 Node-tests en 11 browsergroepen opnieuw uitgevoerd | Geen blokkerende bevindingen |

Tijdens aanvullende verificatie gevonden en opgelost: te laag contrast van het decoratieve sectienummer, ontbrekende pijl-glyphs in systeemfonts en een foutieve option-sluiting in de contactkeuzelijst. Voor de keuzelijst is een browserassertie toegevoegd. De screenshotprocedure scrollt vóór vastleggen direct naar boven om volledige pagina's correct weer te geven.

De eerste axe-injectie werd door de bestaande Content Security Policy geblokkeerd. De testrunner voert axe nu via de DevTools-evaluatiecontext uit; de pagina-CSP is niet versoepeld. Dit is testinstrumentatie, geen wijziging van het veiligheidsbeleid voor bezoekers.

Beperkingen: Chromium getest, geen Safari/Firefox of fysieke apparaten. Geen volledige screenreader- of handmatige WCAG-audit, juridisch onderzoek of certificering. Geen backend of e-mailaflevering aanwezig of getest. Geen bouwstap nodig voor deze statische site. Alle 22 rollen zijn geconfigureerd, maar niet alle 22 live gestart; configuratie is geen bewijs van runtime-activatie. Twee taakgerichte subagents zijn in deze sessie daadwerkelijk gebruikt voor configuratie en onafhankelijke review.

De browsertest start en stopt een tijdelijke server. Screenshots en testresultaat-JSON staan buiten de repository in `/tmp/involfit-browser/`. Alleen fictieve formuliergegevens gebruikt. Er is geen hosting/deploymentworkflow toegevoegd.

## Aanvullende previewgate

De aangescherpte oplevervoorwaarde vereist een gecontroleerde externe previewlink plus GitHub-link en desktop-/mobiele screenshots. De lokale testresultaten blijven geldig; de status is **niet reviewbaar opgeleverd** zolang die externe link ontbreekt. Zie [actuele reviewstatus en screenshots](review/README.md). Geen productiepublicatie.
