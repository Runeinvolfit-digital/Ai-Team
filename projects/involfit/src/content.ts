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
export const experience: readonly Experience[] = [];
