const form = document.querySelector('#contact-form');
const formStatus = form.querySelector('.form-status');
const alert = form.querySelector('.form-error');
const button = form.querySelector('button[type="submit"]');
const fields = ['name', 'email', 'organization', 'message'];

const topics = new Map([
  ['interimmanagement', 'interimmanagement'],
  ['organisatieadvies', 'organisatieadvies'],
  ['verbetering', 'organisatieverbetering'],
  ['trainingen', 'trainingen'],
]);
const topic = topics.get(new URLSearchParams(location.search).get('onderwerp'));
if (topic) form.elements.message.value = `Ik wil graag kennismaken over ${topic}.\n\n`;

function showFieldError(name, message = '') {
  const field = form.elements.namedItem(name);
  form.querySelector(`#${name}-error`).textContent = message;
  if (message) field.setAttribute('aria-invalid', 'true');
  else field.removeAttribute('aria-invalid');
}

form.addEventListener('input', event => {
  if (fields.includes(event.target.name)) showFieldError(event.target.name);
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (button.disabled) return;
  formStatus.textContent = '';
  alert.textContent = '';
  fields.forEach(name => showFieldError(name));
  button.disabled = true;
  formStatus.textContent = 'Bericht wordt verstuurd…';
  try {
    const response = await fetch(form.action, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
      signal: AbortSignal.timeout(16000),
    });
    const result = await response.json();
    formStatus.textContent = '';
    if (response.ok && result.ok === true) {
      form.reset();
      formStatus.textContent = 'Uw bericht is verstuurd. Bedankt voor uw bericht.';
      return;
    }

    alert.textContent = result.message || 'Versturen is niet gelukt. Probeer het opnieuw of mail rechtstreeks.';
    const invalid = fields.filter(name => typeof result.errors?.[name] === 'string');
    invalid.forEach(name => showFieldError(name, result.errors[name]));
    if (invalid.length) form.elements.namedItem(invalid[0]).focus();
  } catch {
    formStatus.textContent = '';
    alert.textContent = 'De verzendstatus is onbekend. Mail rechtstreeks als u geen reactie ontvangt.';
  } finally {
    button.disabled = false;
  }
});
button.disabled = false;
