# Involfit Management & Advies

Persoonlijke website voor Sander de Ridder met Home, Over Sander, Diensten, Ervaring en Contact. Astro bouwt de pagina’s vooraf. Contact verloopt via een directe zakelijke e-maillink.

## Lokaal starten

Gebruik Node.js 24 of hoger en npm.

```bash
npm ci
npm run check
npm test
npm run build
npm start
```

De Node-server luistert standaard op poort 3000. Gebruik `HOST` en `PORT` voor een ander luisteradres. Bouw opnieuw na wijzigingen aan de Astro-pagina’s en publieke assets. In een sandbox zonder schrijfrechten voor de gebruikersconfiguratie kan Astro draaien met `ASTRO_TELEMETRY_DISABLED=1`.

De browsercheck gebruikt Python Playwright en Chromium. Draai na de build:

```bash
python3 tests/browser.py --screenshots /tmp/involfit-review
```

## Inhoud en vrijgave

- Plaats Sanders goedgekeurde portret als `src/assets/sander.jpg` (ook PNG, WebP of AVIF mogelijk). Astro maakt responsieve WebP-varianten. Zonder bestand toont Home alleen de introductie.
- Ervaring toont werkgebieden zolang er geen bevestigde opdrachten zijn. Vul `experience` in `src/content.ts` in, meest recente eerst, met periode, rol, opdracht en eventueel een openbare organisatienaam.
- Bevestig de bio, de dienstnamen en het bestaande zakelijke adres `info@involfit.nl` vóór publicatie.
- Staging is standaard gemarkeerd als `noindex`. Zet `SITE_INDEXABLE` pas na goedgekeurde publicatie op `1`.
- Het bestaande formulierendpoint blijft beschikbaar voor compatibiliteit. De website linkt er niet naar en configureert geen mailprovider voor deze versie. Zie de vorige projectversie voor de endpointconfiguratie.

De [reviewmap](review/) bevat het beeld- en testbewijs. Het eerdere werktafelontwerp staat in de Git-geschiedenis.
