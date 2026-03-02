/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TechriseAnimations = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    start: function () {
        var self = this;
        this._super.apply(this, arguments);

        // Mark JS as ready so CSS animations activate
        document.body.classList.add('tr-js-ready');

        // Force dark navbar immediately
        self._forceNavbarDark();

        // Small delay to let page fully render
        setTimeout(function () {
            self._initCounters();
            self._initScrollAnimations();
            self._initNavbarScroll();
            self._initSmoothScroll();
            // Re-apply after Odoo finishes rendering
            self._forceNavbarDark();
        }, 100);
    },

    _initCounters: function () {
        var self = this;
        var counterElements = document.querySelectorAll('.tr-counter');
        var countersAnimated = new Set();

        if ('IntersectionObserver' in window) {
            var counterObserver = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting && !countersAnimated.has(entry.target)) {
                        countersAnimated.add(entry.target);
                        self._animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.3 });

            counterElements.forEach(function (el) {
                counterObserver.observe(el);
            });
        } else {
            counterElements.forEach(function (el) {
                el.textContent = el.getAttribute('data-target');
            });
        }
    },

    _animateCounter: function (el) {
        var target = parseInt(el.getAttribute('data-target'), 10);
        var duration = 2000;
        var startTime = performance.now();

        function update(currentTime) {
            var elapsed = currentTime - startTime;
            var progress = Math.min(elapsed / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            var current = Math.round(target * eased);
            el.textContent = current;
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.textContent = target;
            }
        }
        requestAnimationFrame(update);
    },

    _initScrollAnimations: function () {
        var animateElements = document.querySelectorAll('.tr-animate');

        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animated');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            animateElements.forEach(function (el) {
                observer.observe(el);
            });
        } else {
            animateElements.forEach(function (el) {
                el.classList.add('animated');
            });
        }
    },

    _forceNavbarDark: function () {
        var navy = '#0D1B3E';
        var isHomepage = document.getElementById('wrapwrap') &&
                         document.getElementById('wrapwrap').classList.contains('homepage');

        // On homepage: header is transparent (floats over hero video)
        // On other pages: force navy background
        if (isHomepage) {
            return;
        }

        // Force header background
        var header = document.querySelector('header.tr-navbar, header#top');
        if (header) {
            header.style.setProperty('background-color', navy, 'important');
        }
        // Force ALL nav.navbar elements inside header
        var navbars = document.querySelectorAll('header nav.navbar, header .navbar');
        navbars.forEach(function (nav) {
            nav.style.setProperty('background-color', navy, 'important');
            nav.style.setProperty('background-image', 'none', 'important');
            nav.style.setProperty('border-color', 'transparent', 'important');
        });
        // Force nav links white
        var links = document.querySelectorAll('header .nav-link, header .navbar-nav > li > a');
        links.forEach(function (link) {
            link.style.setProperty('color', '#FFFFFF', 'important');
        });
    },

    _initNavbarScroll: function () {
        var navbar = document.querySelector('.tr-navbar');
        if (navbar) {
            function handleScroll() {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
            window.addEventListener('scroll', handleScroll, { passive: true });
            handleScroll();
        }
    },

    _initSmoothScroll: function () {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                var targetId = this.getAttribute('href');
                if (targetId === '#') return;
                var targetEl = document.querySelector(targetId);
                if (targetEl) {
                    e.preventDefault();
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    },
});

export default publicWidget.registry.TechriseAnimations;
