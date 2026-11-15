document.addEventListener('DOMContentLoaded', () => {
  // Sign-in / register tabs. Without JavaScript the links still work.
  document.querySelectorAll('[data-tab]').forEach((tab) => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      document.querySelectorAll('[data-tab]').forEach((t) => t.classList.toggle('active', t === tab));
      document.querySelectorAll('[data-panel]').forEach((panel) => {
        panel.hidden = panel.dataset.panel !== tab.dataset.tab;
      });
    });
  });

  // Keep the two password fields consistent before submitting.
  const register = document.getElementById('register-form');
  if (register) {
    register.addEventListener('submit', (event) => {
      if (register.password.value !== register.confirm.value) {
        event.preventDefault();
        alert('Passwords do not match.');
      }
    });
  }

  // Live character counter for contact notes.
  const notes = document.getElementById('notes');
  const counter = document.getElementById('notes-count');
  if (notes && counter) {
    const update = () => { counter.textContent = `${notes.value.length}/200`; };
    notes.addEventListener('input', update);
    update();
  }

  // Confirm destructive admin actions.
  document.querySelectorAll('[data-confirm]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (!confirm(link.dataset.confirm)) event.preventDefault();
    });
  });
});
