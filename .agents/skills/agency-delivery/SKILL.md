---
name: agency-delivery
description: Vertaal een agency-opdracht naar afgebakende uitvoering en bewijs.
---

# agency-delivery

Raadpleeg AGENTS.md, knowledge/agent-matrix.md, agency/rules/efficiency.md en agency/rules/task-interpretation.md voor zover nog niet actueel beschikbaar. Voer klein werk met één uitvoerder uit: leg doel, grenzen en tests in enkele zinnen vast. Gebruik templates/task-brief.md alleen bij grotere taken of overdracht. Selecteer alleen noodzakelijke rollen via agency/agents.json. Voer uitvoering en passende gates uit agency/rules/quality.md uit. Bewaar iedere werkende stap volgens agency/rules/github.md. Lever op met templates/delivery.md; vermeld concrete tests, commits en open punten.

Specialisten krijgen minimale zelfstandige context, waar beschikbaar met `fork_turns="none"`. Maximaal twee gelijktijdige uitvoerders voor onafhankelijk werk, geen dubbele opdrachten. Laat alleen de hoofdcoördinator sessies starten. Kies review naar risico; behoud noodzakelijke security- en kwaliteitsgates. Maximaal twee verschillende herstelpogingen per probleem, daarna een duidelijke blokkade. Rapporteer kort; vermeld tokengebruik alleen als de runtime cijfers levert.

Bij websiteoplevering is agency/rules/preview.md verplicht: gecontroleerde previewlink, GitHub-link en desktop-/mobiele screenshots. Zonder werkende preview blijft de status niet reviewbaar opgeleverd. Productie vereist afzonderlijke expliciete goedkeuring.

Bij websiteopdrachten: volg knowledge/design/design.md en agency/rules/design-preferences.md. Vergelijk bij een nieuwe website of herontwerp meerdere richtingen, werk de gekozen richting uit in code en routeer de verantwoordelijkheden volgens agency/rules/delegation.md. Laat de gerealiseerde versie vóór afronding beoordelen met knowledge/quality/acceptance.md. Verwerk en hercontroleer de bevindingen. Rapporteer alleen daadwerkelijk uitgevoerde agents en controles.


Gebruik bij websiteoverdracht de momenten in [de taakbrief](../../../templates/task-brief.md). Verifieer het leidende concept en de startversie vóór wijzigingen. Volg voor een nieuwe website, herontwerp of nieuwe hoofdinteractie [de twee reviewrondes](../../../agency/rules/quality.md#twee-reviewrondes). Koppel bevinding, herstel en hercontrole aan de betreffende versies.
