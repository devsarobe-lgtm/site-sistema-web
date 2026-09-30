(() => {
    'use strict';

    const menuButton = document.querySelector('[data-lp-menu-toggle]');
    const navigation = document.querySelector('[data-lp-navigation]');
    const header = document.getElementById('lp-header');
    const hero = document.querySelector('.lp-hero');
    const heroWave = hero?.querySelector('.lp-hero__wave');
    const backToTop = document.querySelector('[data-lp-back-to-top]');
    const desktopQuery = window.matchMedia('(min-width: 992px)');
    const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    let scheduleHeaderUpdate = () => {};

    if (header && menuButton && navigation) {
        header.classList.add('lp-header--ready');
    }

    if (header) {
        let headerFrame = null;
        let headerBaseHeight = header.getBoundingClientRect().height;

        const updateHeaderSurface = () => {
            headerFrame = null;
            if (!header.classList.contains('lp-header--menu-open')) {
                const measuredHeight = header.getBoundingClientRect().height;
                if (measuredHeight !== headerBaseHeight ||
                    !document.body.style.getPropertyValue('--lp-header-height')) {
                    headerBaseHeight = measuredHeight;
                    document.body.style.setProperty('--lp-header-height', `${measuredHeight}px`);
                }
            }
            const heroHasPassed = !hero || (heroWave
                ? heroWave.getBoundingClientRect().top <= headerBaseHeight
                : hero.getBoundingClientRect().bottom <= headerBaseHeight);
            header.classList.toggle('lp-header--solid', heroHasPassed);
        };

        scheduleHeaderUpdate = () => {
            if (headerFrame !== null) return;
            headerFrame = window.requestAnimationFrame(updateHeaderSurface);
        };

        updateHeaderSurface();
        window.addEventListener('scroll', scheduleHeaderUpdate, { passive: true });
        window.addEventListener('resize', scheduleHeaderUpdate);
        window.addEventListener('pageshow', scheduleHeaderUpdate);
    }

    if (header && menuButton && navigation) {
        const setMenuOpen = (isOpen, restoreFocus = false) => {
            navigation.classList.toggle('is-open', isOpen);
            header.classList.toggle('lp-header--menu-open', isOpen);
            scheduleHeaderUpdate();
            menuButton.setAttribute('aria-expanded', String(isOpen));
            menuButton.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');

            if (restoreFocus) menuButton.focus();
        };

        menuButton.addEventListener('click', () => {
            setMenuOpen(menuButton.getAttribute('aria-expanded') !== 'true');
        });

        navigation.addEventListener('click', (event) => {
            if (!(event.target instanceof Element) || desktopQuery.matches) return;

            const link = event.target.closest('a');
            if (link) {
                setMenuOpen(false);
                if (link.target === '_blank') {
                    menuButton.focus({ preventScroll: true });
                }
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
                setMenuOpen(false, true);
            }
        });

        document.addEventListener('click', (event) => {
            if (event.target instanceof Element && !event.target.closest('#lp-header') &&
                menuButton.getAttribute('aria-expanded') === 'true') {
                setMenuOpen(false);
            }
        });

        desktopQuery.addEventListener('change', () => setMenuOpen(false));
    }

    document.addEventListener('click', (event) => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey ||
            event.shiftKey || event.altKey || !(event.target instanceof Element)) return;

        const link = event.target.closest('a[data-lp-scroll]');
        if (!link || link.hasAttribute('download') || (link.target && link.target !== '_self') ||
            link.origin !== window.location.origin || link.pathname !== window.location.pathname ||
            link.search !== window.location.search || !link.hash) return;

        const target = document.getElementById(link.hash.slice(1));
        if (!target) return;

        event.preventDefault();
        if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
        target.scrollIntoView({
            behavior: reducedMotionQuery.matches ? 'auto' : 'smooth',
            block: 'start',
        });
        target.focus({ preventScroll: true });
        if (window.location.hash !== link.hash) window.history.pushState(null, '', link.hash);
    });

    if (backToTop) {
        const updateBackToTop = () => {
            backToTop.hidden = window.scrollY < 400;
        };

        window.addEventListener('scroll', updateBackToTop, { passive: true });
        updateBackToTop();

        backToTop.addEventListener('click', () => {
            document.querySelector('.lp-header__brand')?.focus({ preventScroll: true });
            window.scrollTo({
                top: 0,
                behavior: reducedMotionQuery.matches ? 'auto' : 'smooth',
            });
        });
    }

    const partnersSections = document.querySelectorAll('[data-lp-partners]');
    if (partnersSections.length) {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.setAttribute('data-lp-partners-active', '');
                    observer.unobserve(entry.target);
                });
            }, { threshold: 0.1 });

            partnersSections.forEach((section) => observer.observe(section));
        } else {
            partnersSections.forEach((section) => section.setAttribute('data-lp-partners-active', ''));
        }
    }
})();
