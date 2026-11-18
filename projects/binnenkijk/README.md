# Binnenkijk Makelaars

Een demonstratiesite voor een makelaar met woningaanbod, een woningdetailpagina en een 360°-tour. De demowoning is fictief. De gevel, zes binnenbeelden en vraagprijs zijn illustratief.

## Starten

Draai vanuit `projects/binnenkijk` een statische HTTP-server. Er is geen buildstap.

```bash
python3 -m http.server 43831
```

Open de root van de server. Kies de Utrechtse stadswoning en start de rondleiding. In de tour kunt u slepen, de pijltoetsen gebruiken, via doorgangen naar aangrenzende ruimtes gaan en direct een kamer of verdieping kiezen.

## Ontwerp en werking

Een fotoreeks is eenvoudig door te bladeren, maar toont vooral vooraf gekozen standpunten. Een aanklikbare plattegrond helpt met oriëntatie, maar geeft beperkt zicht op de ruimte zelf. Voor deze demo is per ruimte een 360°-panorama gekozen. Dat maakt zelfstandig rondkijken mogelijk en toont hoe ruimtes met elkaar verbonden zijn. Op desktop staat de lijst naast het panorama. Op mobiel staat ze eronder.

De tour modelleert de doorgangen als verbindingen tussen zes panoramastandpunten. Per hotspot is de horizontale positie op het panoramabeeld instelbaar. Bij hardware of browsers zonder WebGL blijven de kamerkiezer en de fotoweergave beschikbaar.

Voor een echte woning zijn een gevelbeeld, feitelijke woninggegevens en een 2:1 equirectangulaire 360°-opname per standpunt nodig. De demo gebruikt gegenereerde beelden in WebP en heeft geen persoonsgegevens of boekingsformulier.

## Testen

Gebruik Python Playwright en Chromium. Start de server en draai:

```bash
python3 tests/browser.py
```

Stel desgewenst `CHROMIUM_PATH` in. De browsercheck maakt volledige screenshots, controleert de route van aanbod naar tour en test de weergave zonder WebGL. Zie het [reviewverslag](review/README.md).
