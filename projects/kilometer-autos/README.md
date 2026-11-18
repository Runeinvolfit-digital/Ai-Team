# Kilometer Auto’s

Een fictieve occasionshowroom met twee demoauto’s. Het aanbod filtert op merk, budget en brandstof. Elke auto heeft een detailpagina met acht opeenvolgende buitenaanzichten, een interieurfoto, specificaties en een proefritdemonstratie.

## Lokaal draaien

Start vanuit deze map een statische HTTP-server. Er is geen buildstap.

```bash
python3 -m http.server 43832
```

De buitenweergave draait met de vorige- en volgende-knoppen, de pijltoetsen of door te slepen. De demo gebruikt gegenereerde beelden en fictieve merken, prijzen en specificaties. De proefritdemonstratie toont een keuze in de pagina. Er worden geen persoonsgegevens gevraagd en er gaat geen aanvraag naar een server.

## Ontwerprichting

Het lichte catalogusconcept maakte het vergelijken gemakkelijk, maar had weinig showroomkarakter. De gekozen donkere richting combineert de grote studiofoto met contrastrijke specificaties, rustige aanbodrijen en bronzen accenten. Op mobiel staan de auto en de bediening boven de specificaties.

## Testen

Gebruik Python Playwright en Chromium. Start de server en draai:

```bash
python3 tests/browser.py
```

De test controleert beide auto’s, de filters, alle acht buitenhoeken, de proefritdemo en de weergave op drie schermbreedtes. Zie de [reviewmap](review/) voor de volledige pagina-opnamen.
