export const cars = [
  { id: 'aurelio-gt', name: 'Aurelio GT', make: 'Aurelio', type: 'Grand tourer', year: 2021,
    distance: 38000, price: 64950, fuel: 'Benzine', color: 'Diepgroen' },
  { id: 'veldt-touring', name: 'Veldt Touring', make: 'Veldt', type: 'Stationwagen', year: 2022,
    distance: 46500, price: 42950, fuel: 'Hybride', color: 'Metallic zilver' },
];

export const money = amount => new Intl.NumberFormat('nl-NL', {
  style: 'currency', currency: 'EUR', maximumFractionDigits: 0,
}).format(amount);
export const mileage = amount => `${amount.toLocaleString('nl-NL')} km`;
export const carImage = (id, view) => new URL(`./assets/${id}-${view}.webp`, import.meta.url).href;
