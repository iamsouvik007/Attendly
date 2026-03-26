/* ============================================================
   ATTENDLY — Micro-animations & Interactivity
   ============================================================ */

(function () {
    'use strict';

    /* ---------- Navbar scroll shadow ---------- */
    var nav = document.querySelector('.site-nav');
    if (nav) {
        window.addEventListener('scroll', function () {
            nav.classList.toggle('scrolled', window.scrollY > 8);
        }, { passive: true });
    }

    /* ---------- Active nav link ---------- */
    var path = window.location.pathname;
    document.querySelectorAll('.nav-links a').forEach(function (link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });

    /* ---------- Hamburger menu ---------- */
    var hamburger = document.getElementById('hamburger');
    var navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('open');
            navLinks.classList.toggle('open');
        });

        // Close menu on link click
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                hamburger.classList.remove('open');
                navLinks.classList.remove('open');
            });
        });
    }

    /* ---------- Button ripple effect ---------- */
    document.querySelectorAll('.btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            var rect = btn.getBoundingClientRect();
            var ripple = document.createElement('span');
            ripple.className = 'ripple';
            var size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            btn.appendChild(ripple);
            ripple.addEventListener('animationend', function () {
                ripple.remove();
            });
        });
    });

    /* ---------- Scroll-reveal: IntersectionObserver ---------- */
    var reveals = document.querySelectorAll('.card, section, .table-wrap');
    if (reveals.length && 'IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('reveal', 'visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

        reveals.forEach(function (el) {
            // Only add reveal if not already visible (above fold)
            var rect = el.getBoundingClientRect();
            if (rect.top > window.innerHeight * 0.85) {
                el.classList.add('reveal');
                revealObserver.observe(el);
            }
        });
    }

    /* ---------- Staggered KPI cards ---------- */
    var grids = document.querySelectorAll('.grid');
    if (grids.length && 'IntersectionObserver' in window) {
        var staggerObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('stagger', 'visible');
                    staggerObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        grids.forEach(function (grid) {
            grid.classList.add('stagger');
            staggerObserver.observe(grid);
        });
    }

    /* ---------- Smooth form focus transitions ---------- */
    document.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.addEventListener('focus', function () {
            if (el.parentElement.classList.contains('input-group')) {
                el.parentElement.classList.add('focused');
            }
        });
        el.addEventListener('blur', function () {
            if (el.parentElement.classList.contains('input-group')) {
                el.parentElement.classList.remove('focused');
            }
        });
    });

})();
