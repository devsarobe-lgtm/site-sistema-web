(() => {
    'use strict';

    const section = document.querySelector('[data-tax-help]');
    if (!section) return;

    const items = [...section.querySelectorAll('.tax-help__item')];

    items.forEach((item) => {
        item.addEventListener('toggle', () => {
            if (item.open) {
                items.forEach((other) => {
                    if (other !== item) other.open = false;
                });
            }

            if (window.AOS && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                window.requestAnimationFrame(() => window.AOS.refresh());
            }
        });
    });

    section.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape' || !(event.target instanceof Element)) return;

        const item = event.target.closest('.tax-help__item');
        if (!item?.open) return;

        item.open = false;
        item.querySelector('summary')?.focus();
        event.preventDefault();
    });
})();
