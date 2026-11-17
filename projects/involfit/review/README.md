# Review van het Involfit-herontwerp

De afbeeldingen tonen de lokale productiebuild van het herontwerp op `site/involfit`, bekeken in Chromium op 17 november 2026. Desktop is 1440 × 1000 CSS-pixels en mobiel is 390 × 844 CSS-pixels. De screenshots tonen de volledige pagina.

| Pagina | Desktop | Mobiel |
| --- | --- | --- |
| Home | [Desktop](home-desktop.png) | [Mobiel](home-mobiel.png) |
| Diensten | [Desktop](diensten-desktop.png) | [Mobiel](diensten-mobiel.png) |
| Contact | [Desktop](contact-desktop.png) | [Mobiel](contact-mobiel.png) |

## Onafhankelijk ontwerpoordeel

De QA-agent beoordeelde de werkende productiebuild en had geen aandeel in het ontwerp of de implementatie. De onderzoeksagent controleerde de openbare en interne inhoudsbronnen. De hoofdcoördinator koos de ontwerprichting, bouwde de site en draaide build-, server- en Lighthouse-controles.

| Onderdeel | Gewicht | Cijfer | Waargenomen bewijs |
| --- | ---: | ---: | --- |
| Visuele identiteit en originaliteit | 20% | 9,1 | Werktafel met vraagstukken over mandaat, besluitvorming en overdracht. Het papierbeeld en de kleurcontrasten horen bij hetzelfde redactionele geheel. |
| UX en gebruiksvriendelijkheid | 20% | 8,8 | De geselecteerde situatie toont een eerste stap en geeft routes naar de dienst en een contactformulier met vooringevuld onderwerp. |
| Visuele afwerking en consistentie | 15% | 8,8 | Samenhangende typografie, kleuren en zichtbare toestanden op de drie hoofdpagina’s. De QA-agent inspecteerde desktop- en mobiele opnamen. |
| Mobiele ervaring | 15% | 9,0 | De drie keuzes blijven boven het antwoord staan. Reflow, tikbediening en 200% tekstvergroting zijn gecontroleerd. |
| Technische kwaliteit | 15% | 8,5 | De typecontrole, productiebuild en vijf HTTP-tests slagen. Het formulier is getest met een geïnjecteerde provider. Live bezorging blijft open. |
| Performance en toegankelijkheid | 10% | 9,4 | Lokale Lighthouse-metingen, tien axe-scans en handmatige toetsing van onder meer focus, toetsenbord, touch, reduced motion en gedrag zonder JavaScript. |
| Content en SEO | 5% | 8,5 | Concrete taakgerichte copy, aantoonbare gegevens uit de projectbronnen, canonical en metadata. De publieke inhoudsbron was geblokkeerd. |

**Gewogen totaal: 8,89/10.** Dit is een intern oordeel over de gerealiseerde versie. Een externe preview, definitieve contentcontrole door de eigenaar en een live verzendtest blijven open.

## Verificatie

Voer vanuit `projects/involfit` de volgende commando’s uit. De browsercontrole gebruikt Python Playwright en Chromium. Met `CHROMIUM_PATH` is een ander uitvoerbaar bestand te kiezen.

```bash
npm ci
npm run check
npm test
npm run build
python3 tests/browser.py --axe /pad/naar/axe.min.js --screenshots review --results review/test-results.json
```

De browsertests gebruikten de lokale HTTP-server. De formuliercontrole omvatte clientvalidatie, servervalidatie, status 503 bij ontbrekende instellingen en status 200 bij acceptatie door een gesimuleerde provider. De [browserresultaten](test-results.json) leggen de geteste breedtes en interacties vast.

Lighthouse 13.6.0 draaide tegen de productiebuild op loopback, met gesimuleerde mobiele throttling en de site alleen voor deze meting indexeerbaar. Zie [meetgegevens](lighthouse.json). De metingen beschrijven laboratoriumgedrag. Praktijkmetingen en INP ontbreken.

## Herstel en open punten

- De eerste mobiele versie plaatste het geopende antwoord tussen de keuzes. De hercontrole gebruikt een native radiogroep die alle keuzes boven het antwoord houdt. De privacykop en lange dienstennamen zijn aangepast na reflow- en tekstvergrotingstests.
- De uitgaande proxy weigert `api.resend.com` met CONNECT 403. De cloud heeft geen testkey of geverifieerde afzender. Gebruik de [stagingstappen](../README.md#veilige-uitrol) voor een echte verzendtest.
- De dependencyvrije Node-runtime heeft geen productieafhankelijkheden. Het open picomatch-advies GHSA-fc5q-39xc-vjpf geldt voor de bouwtools. Bouw uit vertrouwde bronbestanden en lever aan de runtime alleen het productie-artifact en de server.
- De cloud biedt alleen een SSH-portal. De externe previewcheck is geblokkeerd. Deze screenshots komen uit de lokale testversie. Er is geen uitrol naar productie uitgevoerd.
