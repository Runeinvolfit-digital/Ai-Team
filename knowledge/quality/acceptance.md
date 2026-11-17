# Kwaliteitsgate en acceptatie

Eigenaar: QA & Security Lead · versie 1.1

Stel vóór de taak toetsbare criteria vast. Controleer de gevraagde functionaliteit, gevolgen voor bestaande flows, responsive gedrag, touch, toetsenbord, semantiek en relevante WCAG 2.2 AA-criteria. Beoordeel performance, SEO, security en privacy naar risico. Voer beschikbare build-, lint- en testchecks uit wanneer passend.

## Gewogen websitebeoordeling

Beoordeel iedere nieuwe of herontworpen website op de gerealiseerde versie. Bij een gerichte wijziging hercontroleer je de betrokken criteria en vermeld je voor welke ongewijzigde onderdelen bestaand bewijs nog geldig is. Gebruik het [reviewtemplate](../../templates/quality-review.md).

| Onderdeel | Gewicht | Bewijs |
|---|---:|---|
| Visuele identiteit en originaliteit | 20% | Klantcontext, conceptkeuze, herkenbaarheid en beeldfit |
| UX en gebruiksvriendelijkheid | 20% | Primaire taak, navigatie, feedback en foutafhandeling |
| Visuele afwerking en consistentie | 15% | Hiërarchie, witruimte, compositie en interactieve toestanden |
| Mobiele ervaring | 15% | Schermafbeeldingen, leesvolgorde, touch en overflow |
| Technische kwaliteit | 15% | Build, tests en betrouwbaar gedrag van kernfunctionaliteit |
| Performance en toegankelijkheid | 10% | Meetmethode, toetsenbord, focus, contrast en relevante WCAG-controles |
| Content en SEO | 5% | Broncontrole, begrijpelijkheid en relevante SEO-controles |

Geef elk onderdeel een cijfer van 0–10 met een concrete bevinding en bewijs. Vermenigvuldig ieder cijfer met zijn gewicht als fractie en tel de bijdragen op. Gebruik het ongeronde totaal bij de beoordeling. **8,5/10** is het interne opleverdoel. Bij een lagere score kies je gerichte verbeteringen, voer je die uit en herbeoordeel je de betrokken onderdelen. Vermeld een resterend tekort expliciet. Leg bij ontbrekend bewijs vast wat niet is beoordeeld. Een onvolledige review krijgt geen totaalscore.

## Blokkades en rapportage

Kritieke beveiligingsproblemen, kapotte kernfunctionaliteit en ernstige toegankelijkheidsproblemen blokkeren oplevering ongeacht de score. Gegevensverlies of onbevestigde werking van kernflows blijft een open releaseblokkade. De [previewgate](../../agency/rules/preview.md) geldt afzonderlijk. Productiepublicatie vereist toestemming.

Rapporteer per criterium de testmethode, het werkelijke resultaat, de bewijslocatie, het open risico en de eigenaar. Meld welke reviewers en tests werkelijk zijn uitgevoerd. Gebruik de gewogen score als intern oordeel en beperk claims over conformiteit tot daadwerkelijk geteste criteria.
