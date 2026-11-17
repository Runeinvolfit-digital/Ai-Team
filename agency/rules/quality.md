# Kwaliteitsgates

| Gate | Verplicht wanneer | Bewijs |
|---|---|---|
| Scope en kennisbehoud | Deze agency-herbouw | Checker en Git-diff zonder knowledge-wijziging |
| Configuratie | Agent/skill/templatewijziging | TOML parsing, 22 unieke rollen, bestaande kennisreferenties |
| Functioneel | Website/interactie | Navigatie, filtering, formulier ongeldige/geldige invoer in browser |
| Responsief/toegankelijkheid | UI | Smal/breed scherm, toetsenbord, focus, labels, geen overflow, reduced motion |
| Integratie | Codewijziging | Beschikbare build/tests; geen nul-tests als succes |
| Security/privacy | Datastroom | Geen secrets, geen onverwachte requests, feitelijke fout/succesmelding |
| Preview | Websiteoplevering | Gecontroleerde preview-URL, GitHub-link, desktop-/mobiele screenshots volgens preview.md |
| Overdracht | Iedere werkende stap | Commit, push en remote SHA-verificatie |

Rapporteer passed, failed, skipped en niet uitgevoerd apart. Benoem reproduceerbare tekortkomingen. Meet geen fictieve scores. Mislukte verplichte checks vragen diagnose; pas geen tests aan om fouten te verbergen. Reviews zijn proportioneel en begrensd.

Kies alleen gates die bij het risico passen volgens [efficiency.md](efficiency.md). Klein tekstwerk krijgt gerichte controle; geen volledige audit of aparte reviewersessie zonder toegevoegde waarde. Noodzakelijke security- en kwaliteitscontroles blijven verplicht. Maximaal twee verschillende herstelpogingen per probleem; daarna een onderbouwde blokkade en verder met onafhankelijk werk.

Bij een ontbrekende of falende preview is de status niet reviewbaar opgeleverd, ook als lokale tests slagen. Volg [de previewgate](preview.md); productie vereist aparte expliciete goedkeuring.
