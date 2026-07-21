(function() {
  'use strict';

  // === Header scroll effect ===
  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero');

  function onScroll() {
    if (!header) return;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollY > 80) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // === Mobile menu toggle ===
  var menuToggle = document.querySelector('.menu-toggle');
  var mainNav = document.querySelector('.main-nav');

  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      mainNav.classList.toggle('open');
    });
  }

  // === Dropdown on mobile ===
  var dropdowns = document.querySelectorAll('.dropdown');
  dropdowns.forEach(function(dd) {
    var link = dd.querySelector('a');
    if (link && window.innerWidth <= 768) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        dd.classList.toggle('open');
      });
    }
  });

  // === Language dropdown toggle ===
  var langDropdown = document.querySelector('.lang-dropdown');
  var langBtn = document.querySelector('.lang-dropdown-btn');
  if (langBtn) {
    langBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      langDropdown.classList.toggle('open');
    });
    document.addEventListener('click', function() {
      langDropdown.classList.remove('open');
    });
  }

  // === Smooth scroll for anchor links ===
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // === Scroll Animations (Intersection Observer) ===
  var animatedElements = document.querySelectorAll('.animate-on-scroll');

  if ('IntersectionObserver' in window && animatedElements.length > 0) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    animatedElements.forEach(function(el) {
      observer.observe(el);
    });
  } else {
    animatedElements.forEach(function(el) {
      el.classList.add('animated');
    });
  }

  // === Counter animation ===
  function animateCounters() {
    var counters = document.querySelectorAll('.stat-number');
    if (counters.length === 0) return;

    counters.forEach(function(counter) {
      var target = parseInt(counter.getAttribute('data-target'), 10);
      if (isNaN(target)) {
        counter.textContent = counter.textContent || '0+';
        return;
      }

      var duration = 1500;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        counter.textContent = Math.floor(eased * target) + '+';
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          counter.textContent = target + '+';
        }
      }

      requestAnimationFrame(step);
    });
  }

  var statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    if ('IntersectionObserver' in window) {
      var statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            animateCounters();
            statsObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });
      statsObserver.observe(statsSection);
      setTimeout(function() {
        var rect = statsSection.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
          animateCounters();
        }
      }, 1000);
    } else {
      animateCounters();
    }
  }
})();
