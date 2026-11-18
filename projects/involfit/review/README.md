# Review van de persoonlijke Involfit-site

De volledige pagina-opnamen zijn gemaakt in de lokale productiebuild in Chromium op 18 november 2026. Desktop gebruikt 1440 × 1000 CSS-pixels en mobiel 390 × 844. De omgeving biedt alleen een SSH-portal. Een externe HTTP-preview kon daarom niet worden gecontroleerd.

| Pagina | Desktop | Mobiel |
| --- | --- | --- |
| Home | [Desktop](home-desktop.png) | [Mobiel](home-mobiel.png) |
| Over Sander | [Desktop](over-sander-desktop.png) | [Mobiel](over-sander-mobiel.png) |
| Diensten | [Desktop](diensten-desktop.png) | [Mobiel](diensten-mobiel.png) |
| Ervaring | [Desktop](ervaring-desktop.png) | [Mobiel](ervaring-mobiel.png) |
| Contact | [Desktop](contact-desktop.png) | [Mobiel](contact-mobiel.png) |
| Privacy | [Desktop](privacy-desktop.png) | [Mobiel](privacy-mobiel.png) |

## Onafhankelijke beoordeling

De creatieve reviewer bekeek alle vijf hoofdpagina’s in Chromium en beoordeelde ze met de eigenaarsrubric.

| Onderdeel | Gewicht | Cijfer |
| --- | ---: | ---: |
| Visuele identiteit en originaliteit | 20% | 8,6 |
| UX en gebruiksvriendelijkheid | 20% | 8,8 |
| Visuele afwerking en consistentie | 15% | 8,5 |
| Mobiele ervaring | 15% | 8,8 |
| Technische kwaliteit | 15% | 8,8 |
| Performance en toegankelijkheid | 10% | 8,0 |
| Content en SEO | 5% | 7,5 |

**Gewogen oordeel: 8,57/10.** Het oordeel is gebaseerd op de conceptvergelijking, lokale screenshots en browsercontrole. Een Lighthouse-meting en volledige WCAG-audit vallen buiten dit bewijs. De reviewer vond Contact op desktop ruim opgezet en bevestigde de mobiele navigatie, de actieve pagina en de contactbestemming.

Een tweede reviewer testte menu en uitklapblokken met toetsenbord en touch, controleerde reduced motion en stelde vast dat de contactlink naar het zakelijke adres verwijst. Er is geen bericht verstuurd. De review leidde tot een preciezere dienstlink die duidelijk maakt dat de bestemming voorlopig een werkgebied toont.

## Verificatie

- De typecontrole, de productiebuild en de vijf Node-tests zijn geslaagd.
- De browsercontrole op de bijgewerkte versie deed 30 layoutchecks op vijf breedtes, inclusief 320 CSS-pixels. Ze controleerde navigatie, zichtbare focus, Escape, touch, uitklapblokken, deeplinks, reduced motion en bediening zonder JavaScript. Zie [testresultaten](test-results.json).
- Sanders portret, de bio, de definitieve diensten, het zakelijke adres en de loopbaanfeiten wachten op inhoudelijke bevestiging. De tijdlijn toont voorlopig werkgebieden.
