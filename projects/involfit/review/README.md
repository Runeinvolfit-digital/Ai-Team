# Review van de persoonlijke Involfit-site

De volledige pagina-opnamen zijn gemaakt in de lokale productiebuild in Chromium op 20 november 2026. Desktop gebruikt 1440 × 1000 CSS-pixels en mobiel 390 × 844. De omgeving biedt alleen een SSH-portal. Een externe HTTP-preview kon daarom niet worden gecontroleerd.

| Pagina | Desktop | Mobiel |
| --- | --- | --- |
| Home | [Desktop](home-desktop.png) | [Mobiel](home-mobiel.png) |
| Over Sander | [Desktop](over-sander-desktop.png) | [Mobiel](over-sander-mobiel.png) |
| Diensten | [Desktop](diensten-desktop.png) | [Mobiel](diensten-mobiel.png) |
| Ervaring | [Desktop](ervaring-desktop.png) | [Mobiel](ervaring-mobiel.png) |
| Contact | [Desktop](contact-desktop.png) | [Mobiel](contact-mobiel.png) |
| Privacy | [Desktop](privacy-desktop.png) | [Mobiel](privacy-mobiel.png) |

## Eerdere onafhankelijke beoordeling van het ontwerp

Op 18 november bekeek de creatieve reviewer alle vijf hoofdpagina’s in Chromium en beoordeelde ze met de eigenaarsrubric.

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
- Op 20 november zijn de homepage zonder portret en de pagina Ervaring met werkgebieden opnieuw getest. In een tijdelijke testbuild zijn ook responsieve portretbestanden en een tijdlijnitem gecontroleerd. De testinhoud is buiten de site gehouden.
- Sanders portret, de bio, de definitieve diensten, het zakelijke adres en de loopbaanfeiten wachten op inhoudelijke bevestiging. De tijdlijn toont voorlopig werkgebieden.

## Herbeoordeling van inhoud en paginaopbouw

De onafhankelijke reviewer controleerde op 20 november de vijf hoofdpagina’s op 1440 en 390 px. Home toont een vraagkiezer, Over Sander een profiel met werkwijze, Diensten een uitklaplijst met een adviespaneel, Ervaring werkgebieden met gelabelde voorbeelden en Contact een mailpaneel. Alle vijf routes laadden zonder horizontale overflow. De route van de vraagkiezer naar een geopend dienstblok en het bijbehorende voorbeeld werkte op desktop en mobiel. De nieuwe pagina-opnamen bovenaan tonen deze herbeoordeelde versie.

De voorbeeldsituaties bevatten geen klantnamen, periodes of resultaten. Voor een chronologische tijdlijn blijven bevestigde loopbaangegevens nodig.

## Portret op de homepage

De huidige opnamen gebruiken een gereconstrueerde webversie van het door de eigenaar in de chat getoonde portret. Het originele bestand was niet beschikbaar in de werkmap. De browsercontrole is na plaatsing opnieuw gedraaid. Daarnaast is bevestigd dat de responsieve WebP op 320, 390 en 1440 px laadt en dat de drie dienstlinks zichtbaar blijven.
