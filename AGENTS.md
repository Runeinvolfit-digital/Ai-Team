# Involfit Digital — Codex instructies
1. Lees `knowledge/README.md`, `knowledge/company/execution-efficiency.md` en voor je rol de relevante documenten in `knowledge/agent-matrix.md`.
2. De eigenaar formuleert het doel; de Manager maakt een korte task brief met acceptatiecriteria. Verzin geen ongevraagde scope.
3. Manager selecteert teams; leads selecteren specialisten. Geen agent inschakelen zonder concrete taak. Als native delegatie niet werkt, centraal uitvoeren zonder gesimuleerde agentresultaten.
4. **Action first**: na beknopte inspectie de kleinste effectieve wijziging implementeren. Niet eindeloos plannen, herlezen of herontwerpen.
5. Gebruik bestaande stack en patronen; beperk afhankelijkheden, contextverbruik en bestandwijzigingen.
6. Schrijf geen claims over tests, browsen, security, benchmarks of voltooiing zonder bewijs.
7. Geef bij blokkades precies aan wat is geprobeerd en wat nodig is; geen herhaalde vrijwel identieke mislukte pogingen.
8. Vraag menselijke goedkeuring voor productiepublicatie, risicovolle verwijdering/migraties, credentials, DNS/rechten en uitgaven.
9. Voer passende checks uit, geef uitslagen en rapporteer open punten. Geen stille fouten.
10. De platform- en veiligheidsregels hebben altijd voorrang.

## Modulaire agencyconfiguratie
- Gebruik `agency/agents.json` voor de 22 rollen en rapportagelijnen, `.codex/config.toml` voor native rolconfiguratie en `agency/README.md` voor de runtimebeperkingen.
- Pas de taakrelevante regels in `agency/rules/` toe. Gebruik de lokale skills in `.agents/skills/` en de templates in `templates/`.
- Bij deze herbouw blijft de bestaande `knowledge/`-map ongewijzigd. Verifieer met `python3 scripts/check-agency.py`.
- Bewaar iedere werkende stap daadwerkelijk op GitHub volgens `agency/rules/github.md`. Geen productiepublicatie.
