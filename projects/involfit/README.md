# Involfit

Bedrijfswebsite voor Involfit B.V. met Home, Diensten, Contact en een privacyverklaring. Astro bouwt de pagina’s vooraf. De Node-server serveert de productiebuild en verwerkt het formulier via de HTTPS-API van Resend.

## Lokaal starten

Gebruik Node.js 24 of hoger en npm.

```bash
cd projects/involfit
npm ci
npm run build
npm start
```

Open `http://localhost:3000`. Gebruik `npm run dev` om in één stap te bouwen en te starten met herladen van de Node-servercode. Draai na wijzigingen aan Astro of publieke assets opnieuw `npm run build`. Gebruik `HOST` en `PORT` om het luisteradres aan te passen.

```bash
npm run check
npm test
```

De Node-tests starten een HTTP-server op een willekeurige lokale poort, met een gesimuleerde mailprovider. Voor de browsercontrole zijn Python Playwright en Chromium nodig. Zie [review](review/README.md) voor de gebruikte commando’s en resultaten.

## Formulier

| Instelling | Functie |
| --- | --- |
| `RESEND_API_KEY` | Resend-sleutel met verzendrechten, uitsluitend op de server bewaren |
| `CONTACT_FROM` | Door Resend geverifieerde afzender, bijvoorbeeld een mailbox op een geverifieerd afzenderdomein |
| `CONTACT_TO` | Ontvanger. Standaard `info@involfit.nl`. Gebruik in staging expliciet een testinbox |
| `CONTACT_ORIGIN` | Toegestane oorsprong van de site, inclusief `https://`, zonder pad |
| `SITE_INDEXABLE` | Alleen bij goedgekeurde livegang op `1` zetten |

Zonder mailconfiguratie meldt het formulier dat verzending tijdelijk niet beschikbaar is. Het directe e-mailadres blijft beschikbaar. De tekstuele e-mail gebruikt het e-mailadres van de inzender als Reply-To. De website bewaart geen kopie van het bericht. De huidige cloud-egress blokkeert `api.resend.com`. Als een testomgeving een HTTPS-proxy vereist, configureer het domein in de toegestane egress en start Node 24 met `NODE_USE_ENV_PROXY=1`.

## Veilige uitrol

1. Maak een gescheiden stagingomgeving vanaf de gecontroleerde commit. Voer `npm ci`, `npm run check`, `npm test` en `npm run build` uit. Start met `npm start`. Een host die enkel statische bestanden serveert ondersteunt de formulierroute niet.
2. Plaats de server achter HTTPS. Stel `CONTACT_ORIGIN` in op de staging-URL, configureer HSTS op de TLS-terminatie en stuur geen formulierinhoud naar proxylogs of monitoring. Staging stuurt standaard `X-Robots-Tag: noindex, nofollow` en blokkeert crawlers via `robots.txt`.
3. Configureer een beperkte testkey, geverifieerde afzender en aparte testinbox. Open de staging-URL, test navigatie en verstuur een bericht met fictieve gegevens. Controleer ontvangst en Reply-To. Controleer bij een geweigerde inzending dat de foutmelding verschijnt en de invoer behouden blijft.
4. De huidige serverlimiet telt per direct verbindingsadres en ook voor de hele instantie. Achter een reverse proxy kunnen bezoekers hetzelfde limiet delen. Stel zo nodig aanvullende, gedeelde begrenzing in op de vertrouwde proxy en toets dit vóór uitrol. De server vertrouwt geen clientgestuurde doorstuurheaders.
5. Bevestig inhoud, afzender, ontvanger en privacy-informatie met de eigenaar, inclusief de daadwerkelijke hosting, verwerkers, eventuele doorgifte en bewaartermijnen. Publiceer pas na expliciete goedkeuring, met productie-instellingen, `CONTACT_ORIGIN=https://involfit.nl` en `SITE_INDEXABLE=1`. Controleer vervolgens sitemap, canonical, HTTPS, headers en bezorging. Bewaar het vorige release-artifact voor rollback.

## Inhoud en ontwerp

De masteropdracht levert de positionering en trainingsthema’s. [Het bestaande project](https://github.com/Runeinvolfit-digital/Ai-Team/blob/8dfbf3d675bf859cd541e86c8ea8f9619bd80040/projects/involfit-interim/README.md) documenteert interimmanagement, organisatieadvies, de naam van de oprichter en het opgegeven contactadres. De publieke bron gaf in deze omgeving een proxy-403. Specifieke werkgevers, cases, kwalificaties, trainingsnamen en resultaten zijn daarom weggelaten. De trainingsvoorbeelden zijn expliciet als oefenvragen beschreven.

Vergeleken zijn een adviesdossier (professioneel, met meer leestijd), een dienstencatalogus (scanbaar, maar afstandelijk) en een redactionele pagina met vraagverkenner (compacte introductie en snelle route vanuit een herkenbare situatie). De laatste richting is uitgewerkt met een warme papierkleur, donkere tekst, een olijfgroen accent en een oorspronkelijke, gegenereerde architectuurillustratie als sfeerbeeld. Op mobiel komt de vraagverkenner direct onder het beeld. De kerninhoud en vraagverkenner werken ook zonder JavaScript. Met JavaScript krijgt de dienstenpagina toetsenbordbedienbare tabs.
