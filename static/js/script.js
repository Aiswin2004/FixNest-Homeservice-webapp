document.addEventListener('DOMContentLoaded', () => {

  // ─── MOBILE HAMBURGER ────────────────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelector('.nav-links');
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navLinks?.classList.toggle('mobile-open');
      hamburger.classList.toggle('open');
    });
  }

  // ─── AUTO-DISMISS MESSAGES ───────────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => alert.remove(), 5000);
  });

  // ─── HERO SCROLL PARALLAX ────────────────────────────────────
  window.addEventListener('scroll', () => {
    const hero = document.querySelector('.hero');
    if (hero) {
      const scrolled = window.pageYOffset;
      hero.style.backgroundPositionY = scrolled * 0.4 + 'px';
    }
  });

  // ─── STICKY HEADER SHADOW ────────────────────────────────────
  const header = document.querySelector('.header');
  window.addEventListener('scroll', () => {
    if (header) {
      header.style.boxShadow = window.scrollY > 10
        ? '0 4px 30px rgba(0,0,0,0.12)'
        : '0 2px 20px rgba(0,0,0,0.08)';
    }
  });
  // ─── SCROLL REVEAL ANIMATION ─────────────────────────────────
  const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.provider-card, .stat-card, .feature-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });
  console.log('FixNest — JavaScript loaded!');
});
