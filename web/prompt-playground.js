const input = document.querySelector('#input');
const result = document.querySelector('#result');
const clean = document.querySelector('#clean');

function normalizePrompt(value) {
  return value
    .trim()
    .replace(/\s+/g, ' ')
    .replace(/([!?.,])\1{2,}/g, '$1');
}

clean.addEventListener('click', () => {
  const text = normalizePrompt(input.value);
  const sections = [
    'Goal: ' + text,
    'Constraints: keep it clear, useful, and safe.',
    'Output format: structured answer with examples when helpful.'
  ];
  result.textContent = sections.join('\n');
});
