document.addEventListener("DOMContentLoaded", () => {
  console.log("🥗 NutriSense AI Loaded");

  // Mark active nav link
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  // Animate progress bars on load
  document.querySelectorAll('.progress-bar-fill').forEach(bar => {
    const target = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => { bar.style.width = target; }, 200);
  });

  // Nav "More" dropdown toggle
  document.querySelectorAll('.nav-dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const dropdown = toggle.closest('.nav-dropdown');
      const wasOpen = dropdown.classList.contains('open');
      document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
      if (!wasOpen) dropdown.classList.add('open');
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
  });

  // ==========================================================
  // SCROLL-REVEAL: fade/slide elements into view as user scrolls
  // ==========================================================
  const revealEls = document.querySelectorAll('.reveal, .reveal-stagger');
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => io.observe(el));
  }

  // ==========================================================
  // COUNT-UP: animate numeric stats from 0 to target on reveal
  // ==========================================================
  const counters = document.querySelectorAll('.count-up');
  if (counters.length) {
    const countIo = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        countIo.unobserve(el);
        const raw = el.dataset.target || el.textContent;
        const match = raw.match(/[\d.]+/);
        if (!match) return;
        const target = parseFloat(match[0]);
        const suffix = raw.replace(match[0], '');
        const duration = 1100;
        const start = performance.now();
        function tick(now) {
          const p = Math.min(1, (now - start) / duration);
          const eased = 1 - Math.pow(1 - p, 3);
          const val = target * eased;
          el.textContent = (target % 1 === 0 ? Math.round(val) : val.toFixed(1)) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    counters.forEach(el => countIo.observe(el));
  }

  // ==========================================================
  // TILT HOVER: subtle 3D tilt on cards that opt in
  // ==========================================================
  document.querySelectorAll('.tilt-hover').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `translateY(-6px) rotateX(${(-y * 6).toFixed(2)}deg) rotateY(${(x * 6).toFixed(2)}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  // ==========================================================
  // PARALLAX BLOBS: ambient blobs drift slightly with scroll
  // ==========================================================
  const blobContainers = document.querySelectorAll('.ambient-blobs');
  if (blobContainers.length) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      blobContainers.forEach(c => {
        c.style.transform = `translateY(${y * 0.08}px)`;
      });
    }, { passive: true });
  }
});
