import { createPanorama } from './panorama.js';

const floors = ['Begane grond', 'Eerste verdieping'];
const rooms = {
  hal: { label: 'Hal', destination: 'de hal', floor: 0, start: 0, doors: [['woonkamer', .44], ['overloop', .56]] },
  woonkamer: { label: 'Woonkamer', destination: 'de woonkamer', floor: 0, start: -1.17, doors: [['hal', .76], ['keuken', .25]] },
  keuken: { label: 'Keuken', destination: 'de keuken', floor: 0, start: .55, doors: [['woonkamer', .66]] },
  overloop: { label: 'Overloop', destination: 'de overloop', floor: 1, start: .28, doors: [['hal', .25], ['slaapkamer', .76], ['badkamer', .54]] },
  slaapkamer: { label: 'Slaapkamer', destination: 'de slaapkamer', floor: 1, start: .83, doors: [['overloop', .79]] },
  badkamer: { label: 'Badkamer', destination: 'de badkamer', floor: 1, start: 0, doors: [['overloop', .46]] },
};

const viewer = document.querySelector('#viewer');
const canvas = document.querySelector('#panorama');
const photo = document.querySelector('#room-photo');
const label = document.querySelector('#room-name');
const controls = document.querySelector('#view-controls');
const hotspotArea = document.querySelector('#hotspots');
const floorList = document.querySelector('#floors');
const roomList = document.querySelector('#rooms');
const tip = document.querySelector('#tip');
const fullscreen = document.querySelector('#fullscreen');
let panorama = createPanorama(canvas);
let selected = '';
let yaw = 0;
let pitch = 0;
let drag = null;
let spots = [];
let ready = false;

function button(text, action) {
  const element = document.createElement('button');
  element.type = 'button';
  element.textContent = text;
  element.addEventListener('click', action);
  return element;
}

function select(id) {
  if (id === selected) return;
  location.hash = id;
  show(id);
}

function dot(a, b) {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function render() {
  if (!panorama || !ready) return;
  const camera = panorama.draw(yaw, pitch);
  if (!camera) return;
  const placed = [];
  for (const { element, direction } of spots) {
    const depth = dot(direction, camera.forward);
    const x = dot(direction, camera.right) / (depth * camera.halfWidth);
    const y = dot(direction, camera.up) / (depth * camera.halfHeight);
    element.hidden = depth <= 0 || Math.abs(x) > .78 || Math.abs(y) > .68;
    if (!element.hidden) {
      const halfWidth = element.offsetWidth / 2;
      const left = Math.max(halfWidth + 8, Math.min(viewer.clientWidth - halfWidth - 8,
        viewer.clientWidth * (.5 + .5 * x)));
      let top = viewer.clientHeight * (.5 - .5 * y);
      while (placed.some(point => Math.abs(left - point.left) < halfWidth + point.halfWidth + 8
        && Math.abs(top - point.top) < 48)) top -= 48;
      element.style.left = `${left}px`;
      element.style.top = `${top}px`;
      placed.push({ left, top, halfWidth });
    }
  }
}

function fallback() {
  canvas.hidden = true;
  photo.hidden = false;
  controls.hidden = true;
  hotspotArea.classList.add('fallback-links');
  for (const { element } of spots) element.hidden = false;
  tip.textContent = 'Kies een ruimte of doorgang om de woning te bekijken.';
}

function show(id) {
  if (!Object.hasOwn(rooms, id) || selected === id) return;
  const room = rooms[id];
  const active = document.activeElement;
  const restoreFocus = active instanceof HTMLElement
    && (roomList.contains(active) || floorList.contains(active) || hotspotArea.contains(active));
  const floorFocus = floorList.contains(active);
  selected = id;
  yaw = room.start;
  pitch = 0;
  ready = false;
  label.textContent = room.label;
  photo.alt = `Panoramabeeld van de ${room.label.toLowerCase()}`;
  const source = new URL(`../assets/${id}.webp`, import.meta.url).href;
  photo.src = source;

  floorList.replaceChildren(...floors.map((name, index) => {
    const tab = button(name, () => {
      if (index !== room.floor) select(Object.keys(rooms).find(key => rooms[key].floor === index));
    });
    tab.setAttribute('aria-pressed', String(index === room.floor));
    return tab;
  }));
  roomList.replaceChildren(...Object.entries(rooms).filter(([, entry]) => entry.floor === room.floor)
    .map(([key, entry]) => {
      const item = button(entry.label, () => select(key));
      item.setAttribute('aria-pressed', String(key === id));
      return item;
    }));

  spots = room.doors.map(([target, longitude]) => {
    const angle = (longitude - .5) * 2 * Math.PI;
    return {
      element: button(`Naar ${rooms[target].destination}`, () => select(target)),
      direction: [Math.sin(angle), -.26, Math.cos(angle)],
    };
  });
  hotspotArea.replaceChildren(...spots.map(spot => spot.element));
  fallback();
  if (restoreFocus) {
    const list = floorFocus ? floorList : roomList;
    list.querySelector('[aria-pressed="true"]')?.focus({ preventScroll: true });
  }

  if (!panorama) return;
  const image = new Image();
  image.onload = () => {
    if (selected !== id || !panorama) return;
    panorama.load(image);
    ready = true;
    canvas.hidden = false;
    photo.hidden = true;
    controls.hidden = false;
    hotspotArea.classList.remove('fallback-links');
    tip.textContent = 'Sleep of gebruik de pijltoetsen om rond te kijken. Kies een doorgang om verder te lopen.';
    render();
  };
  image.src = source;
}

function rotate(horizontal, vertical = 0) {
  yaw = (yaw + horizontal) % (2 * Math.PI);
  pitch = Math.max(-1.35, Math.min(1.35, pitch + vertical));
  render();
}

function followHash() {
  const requested = location.hash.slice(1);
  show(Object.hasOwn(rooms, requested) ? requested : 'woonkamer');
}

canvas.addEventListener('pointerdown', event => {
  if (!event.isPrimary || event.button !== 0) return;
  drag = { id: event.pointerId, x: event.clientX, y: event.clientY };
  canvas.setPointerCapture(event.pointerId);
});
canvas.addEventListener('pointermove', event => {
  if (drag?.id !== event.pointerId) return;
  rotate((drag.x - event.clientX) * .006, (event.clientY - drag.y) * .006);
  drag = { id: event.pointerId, x: event.clientX, y: event.clientY };
});
canvas.addEventListener('lostpointercapture', () => { drag = null; });
canvas.addEventListener('keydown', event => {
  const directions = { ArrowLeft: [-.16, 0], ArrowRight: [.16, 0], ArrowUp: [0, .14], ArrowDown: [0, -.14] };
  if (!Object.hasOwn(directions, event.key)) return;
  event.preventDefault();
  rotate(...directions[event.key]);
});
canvas.addEventListener('webglcontextlost', () => {
  panorama = null;
  fallback();
});
document.querySelector('#left').addEventListener('click', () => rotate(-.22));
document.querySelector('#right').addEventListener('click', () => rotate(.22));
fullscreen.hidden = !document.fullscreenEnabled;
fullscreen.addEventListener('click', async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await viewer.requestFullscreen();
  } catch {
    tip.textContent = 'Volledig scherm is in deze browser niet beschikbaar.';
  }
});
document.addEventListener('fullscreenchange', () => {
  fullscreen.textContent = document.fullscreenElement ? 'Sluit volledig scherm' : 'Volledig scherm';
});
new ResizeObserver(render).observe(viewer);
window.addEventListener('hashchange', followHash);
followHash();
