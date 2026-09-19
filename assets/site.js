// Mobile navigation
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;

  function isCompact() { return window.matchMedia('(max-width: 940px)').matches; }

  function setOpen(open) {
    nav.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  }

  function sync() {
    if (isCompact()) { setOpen(false); }
    else { nav.hidden = false; toggle.setAttribute('aria-expanded', 'false'); }
  }

  toggle.addEventListener('click', function () { setOpen(nav.hidden); });
  window.addEventListener('resize', sync);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isCompact() && !nav.hidden) { setOpen(false); toggle.focus(); }
  });
  sync();
})();

// Contact form — front-end validation only.
// Replace the submit handler with a real POST to your backend or form service.
(function () {
  var form = document.getElementById('case-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    status.hidden = false;
    status.textContent =
      'This form is not connected to a backend yet. Wire it to your intake system before launch.';
    status.focus();
  });
})();
