# GitHub-opslag

Controleer eerst `git status --short`, huidige branch en `git ls-remote origin HEAD`. Controleer schrijven met `git push --dry-run origin HEAD`; dit is voorlopig bewijs. Maak daarna iedere werkende mijlpaal concreet, voer de passende checks uit en commit alleen eigen taakbestanden.

Push naar de werkbranch: `git push -u origin HEAD`. Verifieer de echte remote branch met `git ls-remote origin refs/heads/<branch>` tegenover `git rev-parse HEAD`. Pas een geslaagde push met dezelfde SHA bewijst opslag. Geen force-push, secrets, reset van gebruikerswerk of productiepublicatie.

Meld een pushblokkade direct met exacte operatie en fout, zonder credentials. Bewaar lokaal werk; onderzoek één gerichte diagnose. Vraag alleen de ontbrekende toegang via veilige instellingen. Claim geen GitHub-links naar niet-opgeslagen bestanden.

## Repositorystructuur
Agencyconfiguratie en de gedeelde kennisbank horen op `main`. Iedere website krijgt een eigen branch `site/[projectnaam]`, gemaakt vanaf `main`, en een eigen map `projects/[projectnaam]/`. Bewaar gedeelde agency-updates op `main`; meng geen andere websites in een sitebranch. Een nieuwe branch is geen Git-worktree. Verifieer branch en werkboom vóór wisselen en behoud bestaand werk. Deze architectuurdemonstratie gebruikt `site/involfit-architectuur` en `projects/involfit-architectuur/`.
