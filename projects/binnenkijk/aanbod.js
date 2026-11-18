const price = document.querySelector('#price');
const location = document.querySelector('#location');
const property = document.querySelector('#property');
const result = document.querySelector('#result');
const empty = document.querySelector('#empty');

function updateResults() {
  const matches = (!price.value || Number(price.value) >= 585000)
    && (!location.value || location.value === 'utrecht');
  property.hidden = !matches;
  empty.hidden = matches;
  result.textContent = matches ? '1 woning' : '0 woningen';
}

for (const filter of [price, location]) {
  filter.addEventListener('change', updateResults);
}
document.querySelector('#reset').addEventListener('click', () => {
  price.value = '';
  location.value = '';
  updateResults();
});

const narrow = matchMedia('(max-width: 48rem)');
const toggle = document.querySelector('#filter-toggle');
const fields = document.querySelector('#filter-fields');

function setFilters(open) {
  fields.hidden = !open;
  toggle.setAttribute('aria-expanded', String(open));
}

function updateFilterLayout() {
  toggle.hidden = !narrow.matches;
  setFilters(!narrow.matches);
}
toggle.addEventListener('click', () => setFilters(fields.hidden));
narrow.addEventListener('change', updateFilterLayout);
updateFilterLayout();
