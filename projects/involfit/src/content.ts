export const services = [
  {
    id: 'interimmanagement',
    title: 'Interimmanagement',
    summary: 'Tijdelijke versterking als een rol openvalt of de uitvoering extra aandacht vraagt.',
    situation: 'Er is tijdelijk leiding nodig om prioriteiten scherp te houden en het werk te laten doorgaan.',
    approach: 'We maken afspraken over de rol, het mandaat en de belangrijkste besluiten. Vanaf het begin is duidelijk wie het werk na de interimperiode overneemt.',
    example: 'Een afdelingshoofd vertrekt terwijl de werving nog loopt. Het team heeft iemand nodig die beslissingen neemt en het werk kan overdragen zodra de opvolger begint.',
    question: 'We hebben tijdelijk versterking nodig',
    opening: 'Een rol valt weg. Wat moet doorgaan?',
    firstStep: 'Maak voor de eerstvolgende weken zichtbaar welke besluiten niet kunnen wachten en wie ze tijdelijk mag nemen.',
  },
  {
    id: 'organisatieadvies',
    title: 'Organisatieadvies',
    summary: 'Een onafhankelijke blik op vraagstukken rond organisatie, verandering en samenwerking.',
    situation: 'Teams herkennen het probleem, maar verschillen van mening over de oorzaak of over de volgende stap.',
    approach: 'We brengen de vraag en de verschillende perspectieven in kaart. Daarna bepalen we welke keuzes nodig zijn en bij wie het besluit ligt.',
    example: 'Een organisatie groeit en twee teams krijgen steeds vaker dezelfde vragen. Ze moeten afspreken wie welk werk doet en wie beslist bij twijfel.',
    question: 'We zoeken richting voor een verandering',
    opening: 'Welk besluit schuift steeds door?',
    firstStep: 'Neem één besluit waar meerdere teams op wachten. Bespreek wat nog onzeker is en wie de keuze kan maken.',
  },
  {
    id: 'verbetering',
    title: 'Organisatieverbetering',
    summary: 'Van terugkerend knelpunt naar een concrete verbetering in het dagelijks werk.',
    situation: 'Werk blijft liggen tussen teams, afspraken zijn onduidelijk of hetzelfde knelpunt komt steeds terug.',
    approach: 'We kijken naar een concreet voorbeeld uit het werk. Dat helpt om te bepalen welke afspraak, overdracht of verantwoordelijkheid als eerste aandacht vraagt.',
    example: 'Nieuwe klantvragen blijven liggen tussen intake en uitvoering. Het team volgt enkele aanvragen om te zien welke informatie bij de overdracht ontbreekt.',
    question: 'We willen een knelpunt aanpakken',
    opening: 'Waar blijft het werk liggen?',
    firstStep: 'Volg één recente overdracht. Kijk welk signaal of welke afspraak ontbrak waardoor het werk stilviel.',
  },
] as const;

export const email = 'info@involfit.nl';

interface Experience {
  period: string;
  role: string;
  organization?: string;
  description: string;
}

// Voeg alleen geverifieerde, openbaar te gebruiken opdrachten toe.
export const experience: readonly Experience[] = [
  {
    period: 'September 2025 – heden',
    role: 'Programmamanager informatiehuishouding',
    organization: 'Dienst Uitvoering Onderwijs (DUO)',
    description: 'Ik begeleid de overgang van een tijdelijk programma naar structureel informatiebeheer in de organisatie. Mijn opdracht omvat informatiesystemen, bewustwording en afstemming met de directies en het ministerie van OCW.',
  },
  {
    period: 'December 2023 – juli 2025',
    role: 'Programmamanager Groningse Digitaliseringsstrategie',
    organization: 'Provincie Groningen',
    description: 'Ik richtte het programma voor digitale transformatie in en stuurde het programmateam aan. Met de organisatie en ICT werkte ik aan een meerjarenvisie en aan prioriteiten voor dienstverlening, informatiemanagement en digitalisering.',
  },
  {
    period: 'Mei 2021 – juli 2023',
    role: 'Manager programma’s en projecten en interimmanager Services',
    organization: 'Gemeente Smallingerland',
    description: 'Ik stuurde het team Programma’s en Projecten aan in het fysieke en sociale domein en de bedrijfsvoering. Als lid van het managementteam hield ik me ook bezig met personeelsplanning, portfoliomanagement en programmatisch sturen.',
  },
  {
    period: 'Februari 2019 – september 2020',
    role: 'Interimmanager Noord-Nederland',
    organization: 'ConoScenza B.V.',
    description: 'Ik leidde de dagelijkse bedrijfsvoering in Noord-Nederland en was verantwoordelijk voor programma’s, projecten en opleiding op het gebied van digitale transformatie en werkplekinnovatie.',
  },
  {
    period: 'Mei 2015 – februari 2019',
    role: 'Algemeen directeur Noord-Nederland',
    organization: 'Ordina N.V.',
    description: 'Ik leidde de noordelijke organisatie en werkte aan de regionale positie van Ordina. In die periode groeide het consultingteam van 18 naar 40 medewerkers en kreeg de regio een eigen academie en afstudeercampus.',
  },
  {
    period: 'April 2009 – mei 2015',
    role: 'Strategisch programmamanager',
    organization: 'Centraal Justitieel Incassobureau (CJIB)',
    description: 'Ik begeleidde trajecten rond wetgeving, ICT, organisatiecultuur en huisvesting. Ik werkte onder meer aan de rijkshuisstijl en vervulde ook rollen in demand- en portfoliomanagement.',
  },
];

export const professionalDevelopment = [
  { title: 'Programmasturing als vak', period: '2022–2023' },
  { title: 'Projectmatig werken bij de gemeentelijke overheid', period: '2021–2022' },
  { title: 'Helder en integraal adviseren', period: '2021' },
  { title: 'Agile projectmanagement', period: '2017–2019' },
  { title: 'Managing Successful Programmes (MSP)', period: '2011–2013' },
  { title: 'Leergang projectmanagement B en C (IPMA)', period: '2006–2007' },
  { title: 'Sustainability, Leadership & Responsibility, London Business School', period: '2003–2004' },
  { title: 'Hbo Personeel & Arbeid, richting Strategisch Management', period: '1994–1998' },
] as const;
