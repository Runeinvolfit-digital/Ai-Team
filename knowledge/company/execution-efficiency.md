# Execution & Efficiency Policy — minder ruis, sneller resultaat
Eigenaar: Agency Manager / Technical Lead • versie 1.0

## Kernregels
1. **Resultaat boven discussie.** Vertaal een opdracht binnen enkele zinnen naar concreet gewenst gedrag en acceptatiecriteria; ga daarna uitvoeren.
2. **Inspecteer één keer doelgericht.** Open relevante bestanden en afhankelijkheden, niet herhaaldelijk de hele repo. Werk met bestaande context.
3. **Minimum viable delegation.** Een kleine CSS- of tekstwijziging gebruikt meestal één specialist. Manager en lead hoeven geen aparte modelronde te doen als ze niets toevoegen.
4. **Geen vergader-agenten.** Start reviewers alleen bij echte ambiguïteit, architectuurimpact, veiligheid of vooraf gedefinieerde kwaliteitsgate.
5. **Geen schijnvoortgang.** Maak geen rapport, plan of refactor als de gevraagde functionele verandering nog niet is gemaakt, tenzij implementatie onmogelijk is.
6. **Maak de kleinst passende wijziging.** Geen ongevraagde herbouw, redesign, nieuwe library, dependency of configwijziging.
7. **Gebruik redelijke defaults.** Vraag alleen bij essentiële ontbrekende informatie of risicovolle keuzes; noteer omkeerbare aannames kort.
8. **Stop herhaling.** Bij dezelfde fout maximaal twee duidelijk verschillende diagnose/aanpakpogingen; daarna blocker met exact bewijs en next step.
9. **Geen verzonnen zekerheid.** Claim geen browsertest, securityaudit, prestatiemeting of werkende native agentdelegatie zonder echte uitvoering.
10. **Verifieer proportioneel.** Kleine UI-wijziging: gerichte build/lint, interactie als browser beschikbaar; beveiligingsgevoelige functie: passende auth-/security-/regressietests. Markeer niet-uitgevoerde tests.
11. **Tegenstrijdige reviews?** Eén verantwoordelijke lead kiest op basis van acceptatiecriteria; alleen naar manager/eigenaar escaleren bij onopgeloste impact.
12. **Eindig als klaar.** Geen onnodige vervolgstappen creëren. Rapporteer beknopt wat veranderd is, welke tests slaagden en wat nog openstaat.

## Snelle beslisboom
- Alleen tekst of CSS, laag risico → één uitvoerder, snelle controle.
- Nieuwe UI-component → designer indien ontwerp onduidelijk; developer bouwt en test.
- Nieuwe backend/API/database/auth → technical lead, passende securityreview, tests.
- Publicatie of gegevensverlies → expliciete eigenaarstoestemming.

## Kwaliteitsgrens
Snelheid mag nooit reden zijn om security, privacy, toegankelijkheid of tests die voor de wijziging noodzakelijk zijn over te slaan. 'Klaar' betekent voldaan aan relevante acceptatiecriteria; anders 'gedeeltelijk klaar'.

## Meetpunten
Leg per opdracht alleen indien relevant vast: doorlooptijd, aantal ingeschakelde agents, aantal codewijzigingen, testresultaten, heropeningen. Optimaliseer later op gemeten knelpunten in plaats van intuïtie.
