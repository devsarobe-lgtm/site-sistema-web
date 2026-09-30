(() => {
    'use strict';

    const menuButton = document.querySelector('[data-lp-menu-toggle]');
    const navigation = document.querySelector('[data-lp-navigation]');
    const header = document.getElementById('lp-header');
    const backToTop = document.querySelector('[data-lp-back-to-top]');
    const desktopQuery = window.matchMedia('(min-width: 992px)');

    const focusPageTarget = (link) => {
        if (link.origin !== window.location.origin ||
            link.pathname !== window.location.pathname || !link.hash) return false;

        const target = document.getElementById(link.hash.slice(1));
        if (!target) return false;

        if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
        return true;
    };

    if (header && menuButton && navigation) {
        header.classList.add('lp-header--ready');

        const setMenuOpen = (isOpen, restoreFocus = false) => {
            navigation.classList.toggle('is-open', isOpen);
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
                if (!focusPageTarget(link) && link.target === '_blank') {
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

    document.querySelector('.lp-hero')?.addEventListener('click', (event) => {
        if (!(event.target instanceof Element)) return;
        const link = event.target.closest('a');
        if (link) focusPageTarget(link);
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
                behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
            });
        });
    }
})();
