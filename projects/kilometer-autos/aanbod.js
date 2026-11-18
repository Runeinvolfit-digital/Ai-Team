import { cars, money, mileage, carImage } from './autos.js';

const make = document.querySelector('#make');
const budget = document.querySelector('#budget');
const fuel = document.querySelector('#fuel');
const result = document.querySelector('#result');
const list = document.querySelector('#cars');

function carRow(car) {
  const row = document.createElement('a');
  row.className = 'car-row';
  row.href = `./auto/?model=${car.id}`;
  const img = document.createElement('img');
  img.src = carImage(car.id, 0);
  img.alt = '';
  img.width = 640;
  img.height = 640;
  const info = document.createElement('div');
  const heading = document.createElement('h2');
  heading.textContent = car.name;
  const summary = document.createElement('p');
  summary.textContent = `${car.year} · ${mileage(car.distance)} · ${car.fuel}`;
  info.append(heading, summary);
  const price = document.createElement('div');
  price.className = 'row-price';
  const amount = document.createElement('strong');
  amount.textContent = money(car.price);
  const action = document.createElement('span');
  action.textContent = 'Bekijk auto';
  price.append(amount, action);
  row.append(img, info, price);
  return row;
}

function render() {
  const matches = cars.filter(car => (!make.value || car.make === make.value)
    && (!budget.value || car.price <= Number(budget.value))
    && (!fuel.value || car.fuel === fuel.value));
  result.textContent = matches.length === 1 ? '1 demoauto' : `${matches.length} demoauto’s`;
  list.replaceChildren(...matches.map(carRow));
  if (!matches.length) {
    const empty = document.createElement('p');
    empty.textContent = 'Geen auto’s voldoen aan deze filters.';
    list.append(empty);
  }
}

for (const filter of [make, budget, fuel]) filter.addEventListener('change', render);
document.querySelector('#reset').addEventListener('click', () => {
  for (const filter of [make, budget, fuel]) filter.value = '';
  render();
});
render();
