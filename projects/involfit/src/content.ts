export const services = [
  {
    id: 'interimmanagement',
    title: 'Interimmanagement',
    summary: 'Tijdelijke versterking als een rol openvalt of de uitvoering extra aandacht vraagt.',
    situation: 'Er is tijdelijk leiding nodig om prioriteiten scherp te houden en het werk te laten doorgaan.',
    approach: 'We maken afspraken over de rol, het mandaat en de belangrijkste besluiten. Vanaf het begin is duidelijk wie het werk na de interimperiode overneemt.',
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
