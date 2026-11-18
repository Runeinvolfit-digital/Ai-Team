# Kwaliteitsgates

| Gate | Verplicht wanneer | Bewijs |
|---|---|---|
| Scope en kennisintegriteit | Agencywijziging | Checker en Git-diff met alleen bedoelde kenniswijzigingen |
| Conceptkeuze | Nieuwe website of herontwerp | Klant en doelgroep, meerdere richtingen, keuze met argumenten voor desktop en mobiel |
| Ontwerpbeoordeling | Website vóór afronding | Gewogen rubric, desktop- en mobiel bewijs, bevindingen en hercontrole |
| Configuratie | Agent/skill/templatewijziging | TOML parsing, 22 unieke rollen, bestaande kennisreferenties |
| Functioneel | Website/interactie | Navigatie, filtering, formulier ongeldige/geldige invoer in browser |
| Responsief/toegankelijkheid | UI | Smal/breed scherm, toetsenbord, focus, labels, geen overflow, reduced motion |
| Integratie | Codewijziging | Beschikbare build/tests; geen nul-tests als succes |
| Security/privacy | Datastroom | Geen secrets, geen onverwachte requests, feitelijke fout/succesmelding |
| Preview | Websiteoplevering | Gecontroleerde preview-URL, GitHub-link, desktop-/mobiele screenshots volgens preview.md |
| Overdracht | Iedere werkende stap | Commit, push en remote SHA-verificatie |

Rapporteer passed, failed, skipped en niet uitgevoerd apart. Benoem reproduceerbare tekortkomingen. Meet geen fictieve scores. Mislukte verplichte checks vragen diagnose; pas geen tests aan om fouten te verbergen. Reviews zijn proportioneel en begrensd.

Kies alleen gates die bij het risico passen volgens [efficiency.md](efficiency.md). Klein tekstwerk krijgt gerichte controle; geen volledige audit of aparte reviewersessie zonder toegevoegde waarde. Noodzakelijke security- en kwaliteitscontroles blijven verplicht. Maximaal twee verschillende herstelpogingen per probleem; daarna een onderbouwde blokkade en verder met onafhankelijk werk.

Voor een nieuwe website of herontwerp beoordeelt een reviewer die de beoordeelde uitwerking niet zelf heeft gemaakt het werkende resultaat vóór afronding. Gebruik de [gewogen rubric](../../knowledge/quality/acceptance.md#gewogen-websitebeoordeling) en het [reviewtemplate](../../templates/quality-review.md). De reviewer kan afkeuren op ontwerpkwaliteit, ook bij geslaagde technische tests. De uitvoerder verwerkt onderbouwde bevindingen en controleert de wijzigingen. Gebruik screenshots en browserbewijs waar beschikbaar. Meld ontbrekend bewijs. Wanneer onafhankelijke inzet niet beschikbaar is, voer de inhoudelijke review centraal uit, label die als zelfreview en laat de onafhankelijke controle als open staan. Bij een gerichte wijziging volstaat een review van de impact volgens de rubric.

Bij een ontbrekende of falende preview is de status niet reviewbaar opgeleverd, ook als lokale tests slagen. Volg [de previewgate](preview.md); productie vereist aparte expliciete goedkeuring.

## Twee reviewrondes

Bij nieuwe websites, herontwerpen en nieuwe hoofdinteracties beoordeelt de ontwerpafdeling eerst vanuit merk, UX, tekst en beweging. Gebruik bij de tweede ronde de Critical Reviewer voor scope, aannames en onderbouwing en de First-Time User Tester voor een concrete bezoekerstaak. Beide krijgen de actuele opdracht en de te beoordelen versie. Bij concepten beschrijven ze wat ze in beeld kunnen beoordelen. Op de werkende versie testen ze relevante taken en interacties in de browser.

De coördinator koppelt bevindingen aan een uitvoerder. Leg het herstel vast en laat de relevante bevinding hercontroleren op de aangepaste versie. Gebruik [de taakbrief](../../templates/task-brief.md) voor de overdracht en [het reviewtemplate](../../templates/quality-review.md) voor bewijs.


Gebruik bij terugkoppeling de status open, hersteld en te hercontroleren, hergecontroleerd of uitgesteld met reden. Geef voorrang aan blokkades van de primaire taak en aan security-, privacy- of toegankelijkheidsproblemen. Een hoge ontwerpscore heft zulke blokkades niet op.
