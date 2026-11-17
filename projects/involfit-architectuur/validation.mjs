/** Pure local demo validation. No persistence or network side effects. */
export function validateContact(values) {
  const errors = {};
  const name = String(values.name ?? '').trim();
  const email = String(values.email ?? '').trim();
  const message = String(values.message ?? '').trim();
  if (!name || name.length > 100) errors.name = 'Vul uw naam in (maximaal 100 tekens).';
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = 'Vul een geldig e-mailadres in, bijvoorbeeld naam@example.com.';
  if (message.length < 20 || message.length > 2000) errors.message = 'Beschrijf uw idee in 20 tot 2000 tekens.';
  return errors;
}
