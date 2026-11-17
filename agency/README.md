# Involfit Digital Agency

De bestaande kennisbank blijft de bron. [agents.json](agents.json) koppelt de 22 matrixrollen aan één Manager, vier leads en zeventien specialisten. De native rollen staan in [.codex/config.toml](../.codex/config.toml); rolbestanden bevatten taken, kennisrouting en overdracht.

Start Codex vanuit deze repository en vertrouw projectconfiguratie alleen na eigen beoordeling. Vraag de Manager een afgebakende taak uit te voeren. Native rolselectie gebeurt via het `agent_type` van de spawn-tool, wanneer de gebruikte runtime die aanbiedt. Hosttools kunnen eigen agentrollen hanteren; deze bestanden wijzigen een reeds lopende cloudsessie niet. De aanwezigheid van configuratie bewijst geen 22 actieve processen of succesvolle delegatie. Start alleen noodzakelijke rollen.

## Werkvolgorde
1. Gebruik [opdrachtinterpretatie](rules/task-interpretation.md) en [task brief](../templates/task-brief.md).
2. Manager kiest leads; leads wijzen concrete specialisttaken toe.
3. Gebruik toepasselijke lokale [skills](../.agents/skills/agency-delivery/SKILL.md).
4. Implementeer, toets relevante [kwaliteitsgates](rules/quality.md), bewaar elke werkende stap via [GitHub-regels](rules/github.md).
5. Rapporteer met [oplevertemplate](../templates/delivery.md).

Validatie: `python3 scripts/check-agency.py`. De checker controleert rolstructuur, TOML, kennisrouting, skills/templates en behoud van kennisbestanden. Dit is configuratievalidatie, geen live modeltest.

Schema: https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json (geraadpleegd 2026-11-17). Geen model, credentials of permissies worden in projectconfiguratie overschreven.
