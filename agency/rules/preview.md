# Reviewbare websiteoplevering

Een website is pas **reviewbaar opgeleverd** met alle onderstaande bewijzen. Een werkende lokale server, screenshot of GitHub-bronlink vervangt geen bereikbare previewlink.

Wijs bij de projectstart een previewverantwoordelijke aan. Die controleert vroeg welke testomgeving beschikbaar is en legt een eventuele blokkade vast in de taakbrief.

1. Lever een previewadres op de bedoelde websitebranch. Gebruik een ondersteunde previewomgeving of platformportal; verzin geen URL en presenteer localhost niet als een link die de opdrachtgever kan openen. Een preview is een testomgeving, geen definitieve productiepublicatie.
2. Open het exacte previewadres en controleer dat de bedoelde site daadwerkelijk laadt, zonder foutpagina, ontbrekende assets of onverwachte loginbarrière. Controleer belangrijke pagina's en de primaire interactie op die preview. Een HTTP 200 of een gereserveerde URL alleen bewijst geen werking. Meld toegangseisen en tijdelijke geldigheid.
3. Leg vast: gecontroleerde URL, datum/tijd met tijdzone, branch/broncommit en werkelijk uitgevoerd gedrag. Maak van elke pagina een volledige screenshot van boven tot onder, inclusief footer, op zowel desktop als mobiel. Gebruik voor alle opnamen dezelfde versie; benoem pagina, viewport en of de opname van de externe preview of een lokale test komt. Presenteer lokale screenshots nooit als bewijs van externe bereikbaarheid.
4. Geef bij oplevering de gecontroleerde previewlink, directe GitHub-link naar de sitebranch/projectmap, desktop- en mobiele screenshots en een kort verslag van tests en open punten. Bewaar screenshots en reviewinformatie bij voorkeur in `projects/[projectnaam]/review/` op de sitebranch; geen credentials of persoonsgegevens.
5. Ontbreekt previewtoegang of faalt de controle, meld dan **niet reviewbaar opgeleverd** met de concrete blokkade. Rond onafhankelijk werk af, maar claim geen voltooiing. Vraag alleen de ontbrekende toegang of platforminstelling; voer geen productiepublicatie uit om de preview-eis te omzeilen.
6. Definitieve productiepublicatie vereist vooraf expliciete goedkeuring van de eigenaar voor de concrete versie en bestemming. Een previewopdracht, push, merge of reviewgoedkeuring is geen toestemming voor productie.

Deze gate blijft verplicht bij websiteoplevering, ook binnen de zuinige uitvoeringsstandaard. Een gewijzigde websiteversie vereist een opnieuw gecontroleerde preview en bijpassende screenshots. Voor een beperkte wijziging volstaan gerichte controles; ongewijzigde functies hoeven niet opnieuw volledig getest.


Controleer vóór oplevering of reviewverslag, opnamen en preview naar dezelfde bronversie herleidbaar zijn. Gebruik waar mogelijk de deployreferentie of een bewijslink naar de geteste commit. Noteer welke pagina’s en toestanden de beelden tonen, bijvoorbeeld een geopend mobiel menu bij navigatiefeedback.


Controleer vroeg of de opdrachtgever het testadres kan bereiken met de beoogde toegang. Leg bij een blokkade de eigenaar en de ontbrekende optie of toegang vast. Controleer opnieuw zodra de omgeving of toegang wijzigt. Gebruik lokale browserchecks en screenshots als lokaal bewijs zolang de externe route openstaat.
