/* b347.dev: shared behaviour for the home page and the app pages. */

/* Back-to-top button: shows after scrolling, scrolls up on click. */
(function () {
  var btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    btn.classList.toggle('visible', window.scrollY > 400);
  });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

/* TestFlight slot: data-tf-state="closed" disables the join link. */
(function () {
  document.querySelectorAll('.tf-slot').forEach(function (slot) {
    var link = slot.querySelector('.store-btn');
    if (!link || slot.dataset.tfState === 'open') return;
    link.removeAttribute('href');
    link.setAttribute('aria-disabled', 'true');
    link.setAttribute('aria-label', 'TestFlight beta is currently closed');
    link.setAttribute('tabindex', '-1');
  });
})();
