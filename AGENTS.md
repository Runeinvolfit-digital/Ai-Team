# Involfit Digital — Codex instructies
1. Raadpleeg `knowledge/README.md`, `knowledge/company/execution-efficiency.md` en de relevante rolrij in `knowledge/agent-matrix.md` voor zover nog niet actueel beschikbaar; lees daarna alleen benodigde documenten.
2. De eigenaar formuleert het doel; één uitvoerder legt bij klein werk doel, grenzen en tests in enkele zinnen vast. Manager en teamleiders zijn dan verantwoordelijkheden, geen extra sessies. Verzin geen ongevraagde scope.
3. Gebruik één uitvoerder als standaard. Start alleen nuttige specialisttaken, met minimale taakcontext en maximaal twee gelijktijdige uitvoerders voor onafhankelijk werk. Alleen de hoofdcoördinator start subagents. Als delegatie niet werkt, centraal uitvoeren zonder gesimuleerde agentresultaten.
4. **Action first**: na beknopte inspectie de kleinste effectieve wijziging implementeren. Niet eindeloos plannen, herlezen of herontwerpen.
5. Gebruik bestaande stack en patronen; beperk afhankelijkheden, contextverbruik en bestandwijzigingen.
6. Schrijf geen claims over tests, browsen, security, benchmarks of voltooiing zonder bewijs.
7. Geef bij blokkades precies aan wat is geprobeerd en wat nodig is; geen herhaalde vrijwel identieke mislukte pogingen.
8. Vraag menselijke goedkeuring voor productiepublicatie, risicovolle verwijdering/migraties, credentials, DNS/rechten en uitgaven.
9. Voer passende checks uit, geef uitslagen en rapporteer open punten. Geen stille fouten.
10. De platform- en veiligheidsregels hebben altijd voorrang.

## Modulaire agencyconfiguratie
- Gebruik `agency/agents.json` voor de 22 rollen en rapportagelijnen, `.codex/config.toml` voor native rolconfiguratie en `agency/README.md` voor de runtimebeperkingen.
- Pas de taakrelevante regels in `agency/rules/` toe; `agency/rules/efficiency.md` bepaalt de zuinige uitvoeringsstandaard. Gebruik de lokale skills in `.agents/skills/` en de templates in `templates/`.
- Bij deze herbouw blijft de bestaande `knowledge/`-map ongewijzigd. Verifieer met `python3 scripts/check-agency.py`.
- Bewaar iedere werkende stap daadwerkelijk op GitHub volgens `agency/rules/github.md`. Geen productiepublicatie.
- Hergebruik actuele gelezen kennis; lees opnieuw bij wijzigingen of ontbrekende context. Maximaal twee verschillende herstelpogingen per probleem; daarna een concrete blokkade.
- Rapporteer kort wijziging, echte tests en open punten. Tokengebruik alleen uit beschikbare runtimecijfers; geen verzonnen besparingspercentages.

- Websiteoplevering: pas `agency/rules/preview.md` toe. Pas reviewbaar met gecontroleerde previewlink, GitHub-link en desktop-/mobiele screenshots. Definitieve productiepublicatie vereist expliciete eigenaarstoestemming.

- Voor websiteontwerp gelden de vaste voorkeuren in `agency/rules/design-preferences.md`: geen standaard bovenlabels, buitensporige titels, decoratieve nummers of pijltjes; wel een passende onderscheidende functie met toegankelijke animatie.
