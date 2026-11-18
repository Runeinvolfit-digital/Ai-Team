import { cars, money, mileage, carImage } from '../autos.js';

const requested = new URLSearchParams(location.search).get('model') ?? cars[0].id;
const car = cars.find(entry => entry.id === requested);
const angleNames = ['Schuin van voren links', 'Linkerkant', 'Schuin van achteren links',
  'Achterkant', 'Schuin van achteren rechts', 'Rechterkant', 'Schuin van voren rechts', 'Voorkant'];

function setup(car) {
  const exterior = document.querySelector('#outside');
  const interior = document.querySelector('#inside');
  const image = document.querySelector('#car-image');
  const stage = document.querySelector('#stage');
  const controls = document.querySelector('#controls');
  const angle = document.querySelector('#angle');
  let frame = 0;
  let inside = false;
  let drag = null;

  document.querySelector('#title').textContent = car.name;
  document.title = `${car.name} | Kilometer Auto’s`;
  document.querySelector('#price').textContent = money(car.price);
  const facts = document.querySelector('#facts');
  for (const [name, value] of [
    ['Uitvoering', car.type], ['Bouwjaar', car.year], ['Kilometerstand', mileage(car.distance)],
    ['Brandstof', car.fuel], ['Kleur', car.color],
  ]) {
    const term = document.createElement('dt');
    term.textContent = name;
    const description = document.createElement('dd');
    description.textContent = value;
    facts.append(term, description);
  }

  function show() {
    exterior.setAttribute('aria-pressed', String(!inside));
    interior.setAttribute('aria-pressed', String(inside));
    controls.hidden = inside;
    stage.classList.toggle('interior', inside);
    stage.tabIndex = inside ? -1 : 0;
    stage.setAttribute('aria-label', inside ? 'Interieurfoto' : 'Draai de auto met de pijltoetsen of door te slepen');
    image.src = carImage(car.id, inside ? 'interieur' : frame);
    image.alt = inside ? `Interieur van de ${car.name}` : `${car.name} · ${angleNames[frame]}`;
    angle.textContent = angleNames[frame];
  }

  function turn(step) {
    if (inside) return;
    frame = ((frame + step) % angleNames.length + angleNames.length) % angleNames.length;
    show();
  }

  document.querySelector('#previous').addEventListener('click', () => turn(-1));
  document.querySelector('#next').addEventListener('click', () => turn(1));
  exterior.addEventListener('click', () => { inside = false; show(); });
  interior.addEventListener('click', () => { inside = true; show(); });
  stage.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    turn(event.key === 'ArrowLeft' ? -1 : 1);
  });
  stage.addEventListener('pointerdown', event => {
    if (inside || !event.isPrimary || event.button !== 0) return;
    drag = event.clientX;
    stage.setPointerCapture(event.pointerId);
  });
  stage.addEventListener('pointermove', event => {
    if (drag === null || !event.isPrimary) return;
    const steps = Math.trunc((event.clientX - drag) / 45);
    if (!steps) return;
    drag += steps * 45;
    turn(steps);
  });
  stage.addEventListener('lostpointercapture', () => { drag = null; });
  document.querySelector('#drive-form').addEventListener('submit', event => {
    event.preventDefault();
    const period = new FormData(event.currentTarget).get('period');
    document.querySelector('#drive-status').textContent = `${car.name} · ${period.toLowerCase()}. Dit is een demokeuze.`;
  });

  document.querySelector('#detail').hidden = false;
  show();
  for (let i = 1; i < angleNames.length; i++) {
    const preload = new Image();
    preload.src = carImage(car.id, i);
  }
}

if (car) setup(car);
else {
  document.querySelector('#title').textContent = 'Auto niet gevonden';
  document.querySelector('#missing').hidden = false;
}
