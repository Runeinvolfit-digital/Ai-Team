# Involfit Digital Agency

De bestaande kennisbank blijft de bron. [agents.json](agents.json) koppelt de 22 matrixrollen aan één Manager, vier leads en zeventien specialisten. De native rollen staan in [.codex/config.toml](../.codex/config.toml); rolbestanden bevatten taken, kennisrouting en overdracht.

Start Codex vanuit deze repository en vertrouw projectconfiguratie alleen na eigen beoordeling. Gebruik voor klein werk één uitvoerder die doel, grenzen en tests kort vastlegt; start geen aparte Manager- of teamleidersessie. Native rolselectie gebeurt via het `agent_type` van de spawn-tool, wanneer de gebruikte runtime die aanbiedt. Hosttools kunnen eigen agentrollen hanteren; deze bestanden wijzigen een reeds lopende cloudsessie niet. De aanwezigheid van configuratie bewijst geen 22 actieve processen of succesvolle delegatie. Start alleen noodzakelijke rollen.

## Werkvolgorde
1. Volg de [zuinige uitvoeringsstandaard](rules/efficiency.md) en [opdrachtinterpretatie](rules/task-interpretation.md). Gebruik de [taakbrief](../templates/task-brief.md) alleen bij grotere taken of overdracht.
2. Zet alleen rollen in die iets toevoegen. De hoofdcoördinator start maximaal twee onafhankelijke uitvoerders tegelijk, inclusief zichzelf wanneer die uitvoert; geen geneste delegatie.
3. Gebruik toepasselijke lokale [skills](../.agents/skills/agency-delivery/SKILL.md).
4. Implementeer, toets relevante [kwaliteitsgates](rules/quality.md), bewaar elke werkende stap via [GitHub-regels](rules/github.md).
5. Rapporteer met [oplevertemplate](../templates/delivery.md).

Validatie: `python3 scripts/check-agency.py`. De checker controleert rolstructuur, TOML, kennisrouting, skills/templates en behoud van kennisbestanden. Dit is configuratievalidatie, geen live modeltest.

Schema: https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json (geraadpleegd 2026-11-17). Geen model, credentials of permissies worden in projectconfiguratie overschreven.

De native configuratie begrenst subagentthreads per sessie op twee en delegatiediepte op één. De aanvullende grens van twee actieve uitvoerders is een coördinatieregel; hostgedrag en tokenbesparing zijn daarmee niet bewezen. Meet tokens alleen waar de runtime cijfers geeft. De kennisbank en 22 rollen blijven behouden.

Websiteoplevering volgt de [previewgate](rules/preview.md): gecontroleerde previewlink, GitHub-link en desktop-/mobiele screenshots. Zonder werkende preview is de site niet reviewbaar opgeleverd. Definitieve productiepublicatie vraagt expliciete eigenaarstoestemming.
