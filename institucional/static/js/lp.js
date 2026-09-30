(() => {
    'use strict';

    const menuButton = document.querySelector('[data-lp-menu-toggle]');
    const navigation = document.querySelector('[data-lp-navigation]');
    const backToTop = document.querySelector('[data-lp-back-to-top]');
    const desktopQuery = window.matchMedia('(min-width: 768px)');

    if (menuButton && navigation) {
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
                const target = link.hash && document.getElementById(link.hash.slice(1));
                if (target) target.focus({ preventScroll: true });
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
