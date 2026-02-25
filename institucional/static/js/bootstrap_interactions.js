(() => {
    const NAVBAR_ID = 'mainNavbar';
    const MODAL_IDS = new Set(['privacyModal', 'termsModal']);
    const TRANSITION_MS = 350;

    const isElement = (value) => value instanceof HTMLElement;

    const afterTransition = (element, callback, timeout = TRANSITION_MS) => {
        let done = false;

        const finish = () => {
            if (done) return;
            done = true;
            element.removeEventListener('transitionend', onEnd);
            callback();
        };

        const onEnd = (event) => {
            if (event.target === element) {
                finish();
            }
        };

        element.addEventListener('transitionend', onEnd);
        window.setTimeout(finish, timeout + 50);
    };

    const forceReflow = (element) => element.offsetHeight;

    const setupNavbarCollapse = () => {
        const toggler = document.querySelector('[data-bs-target="#mainNavbar"]');
        const target = document.getElementById(NAVBAR_ID);

        if (!isElement(toggler) || !isElement(target)) return;

        const setExpanded = (expanded) => {
            toggler.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        };

        const show = () => {
            if (target.classList.contains('show') || target.classList.contains('collapsing')) return;

            target.classList.remove('collapse');
            target.classList.add('collapsing');
            target.style.height = '0px';

            forceReflow(target);
            target.style.height = `${target.scrollHeight}px`;
            setExpanded(true);

            afterTransition(target, () => {
                target.classList.remove('collapsing');
                target.classList.add('collapse', 'show');
                target.style.height = '';
            });
        };

        const hide = () => {
            if (!target.classList.contains('show') || target.classList.contains('collapsing')) return;

            target.style.height = `${target.getBoundingClientRect().height}px`;
            forceReflow(target);

            target.classList.add('collapsing');
            target.classList.remove('collapse', 'show');
            target.style.height = '0px';
            setExpanded(false);

            afterTransition(target, () => {
                target.classList.remove('collapsing');
                target.classList.add('collapse');
                target.style.height = '';
            });
        };

        toggler.addEventListener('click', () => {
            if (target.classList.contains('show')) {
                hide();
                return;
            }
            show();
        });
    };

    const setupFaqAccordion = () => {
        const accordion = document.getElementById('faqAccordion');
        if (!isElement(accordion)) return;

        const getTargetFromButton = (button) => {
            if (!isElement(button)) return null;
            const selector = button.getAttribute('data-bs-target');
            if (!selector || !selector.startsWith('#')) return null;
            const target = document.querySelector(selector);
            return isElement(target) ? target : null;
        };

        const getButtonsForTarget = (target) => {
            if (!isElement(target) || !target.id) return [];
            return [...accordion.querySelectorAll('[data-bs-toggle="collapse"][data-bs-target]')].filter((button) => {
                return isElement(button) && button.getAttribute('data-bs-target') === `#${target.id}`;
            });
        };

        const syncButtonState = (target, expanded) => {
            getButtonsForTarget(target).forEach((button) => {
                button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
                button.classList.toggle('collapsed', !expanded);
            });
        };

        const show = (target) => {
            if (!isElement(target) || target.classList.contains('show') || target.classList.contains('collapsing')) return;

            target.classList.remove('collapse');
            target.classList.add('collapsing');
            target.style.height = '0px';

            forceReflow(target);
            target.style.height = `${target.scrollHeight}px`;
            syncButtonState(target, true);

            afterTransition(target, () => {
                target.classList.remove('collapsing');
                target.classList.add('collapse', 'show');
                target.style.height = '';
            });
        };

        const hide = (target) => {
            if (!isElement(target) || !target.classList.contains('show') || target.classList.contains('collapsing')) return;

            target.style.height = `${target.getBoundingClientRect().height}px`;
            forceReflow(target);

            target.classList.add('collapsing');
            target.classList.remove('collapse', 'show');
            target.style.height = '0px';
            syncButtonState(target, false);

            afterTransition(target, () => {
                target.classList.remove('collapsing');
                target.classList.add('collapse');
                target.style.height = '';
            });
        };

        const hideSiblings = (target) => {
            if (!isElement(target)) return;
            const parentSelector = target.getAttribute('data-bs-parent');
            if (!parentSelector || !parentSelector.startsWith('#')) return;

            const parent = document.querySelector(parentSelector);
            if (!isElement(parent)) return;

            [...parent.querySelectorAll('.collapse.show')].forEach((item) => {
                if (!isElement(item) || item === target) return;
                hide(item);
            });
        };

        [...accordion.querySelectorAll('[data-bs-toggle="collapse"][data-bs-target]')].forEach((button) => {
            if (!isElement(button)) return;
            const target = getTargetFromButton(button);
            if (!isElement(target)) return;
            syncButtonState(target, target.classList.contains('show'));
        });

        accordion.addEventListener('click', (event) => {
            const target = event.target;
            if (!(target instanceof Element)) return;

            const button = target.closest('[data-bs-toggle="collapse"][data-bs-target]');
            if (!isElement(button) || !accordion.contains(button)) return;

            if (accordion.querySelector('.collapsing')) return;

            const collapse = getTargetFromButton(button);
            if (!isElement(collapse) || collapse.classList.contains('collapsing')) return;

            event.preventDefault();

            if (collapse.classList.contains('show')) {
                hide(collapse);
                return;
            }

            hideSiblings(collapse);
            show(collapse);
        });
    };

    const setupModals = () => {
        let activeModal = null;
        let activeTrigger = null;
        let activeBackdrop = null;

        const getFocusable = (modal) => {
            if (!isElement(modal)) return [];
            const selector = [
                'a[href]',
                'button:not([disabled])',
                'input:not([disabled])',
                'select:not([disabled])',
                'textarea:not([disabled])',
                '[tabindex]:not([tabindex="-1"])',
            ].join(',');
            return [...modal.querySelectorAll(selector)].filter((item) => isElement(item) && item.offsetParent !== null);
        };

        const createBackdrop = () => {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade';
            document.body.appendChild(backdrop);
            forceReflow(backdrop);
            backdrop.classList.add('show');
            return backdrop;
        };

        const openModal = (modal, trigger) => {
            if (!isElement(modal)) return;

            if (activeModal && activeModal !== modal) {
                closeModal(activeModal, { restoreFocus: false, immediate: true, keepBodyOpen: true });
            }

            activeModal = modal;
            activeTrigger = trigger || null;

            document.body.classList.add('modal-open');

            activeBackdrop = createBackdrop();

            modal.style.display = 'block';
            modal.removeAttribute('aria-hidden');
            modal.setAttribute('aria-modal', 'true');
            modal.setAttribute('role', 'dialog');

            forceReflow(modal);
            modal.classList.add('show');

            const focusable = getFocusable(modal);
            if (focusable.length > 0) {
                focusable[0].focus();
            } else {
                modal.focus();
            }
        };

        const closeModal = (modal, options = {}) => {
            if (!isElement(modal)) return;
            const restoreFocus = options.restoreFocus !== false;
            const immediate = options.immediate === true;
            const keepBodyOpen = options.keepBodyOpen === true;
            const triggerToRestore = activeTrigger;
            const backdropToRemove = activeBackdrop;
            const isClosingActive = activeModal === modal;

            modal.classList.remove('show');
            modal.setAttribute('aria-hidden', 'true');
            modal.removeAttribute('aria-modal');

            if (backdropToRemove) {
                backdropToRemove.classList.remove('show');
            }

            const finalizeClose = () => {
                modal.style.display = 'none';

                if (isClosingActive) {
                    activeModal = null;
                    activeBackdrop = null;
                    activeTrigger = null;
                }

                if (backdropToRemove) {
                    backdropToRemove.remove();
                }

                if (!keepBodyOpen && !activeModal) {
                    document.body.classList.remove('modal-open');
                }

                if (restoreFocus && isElement(triggerToRestore)) {
                    triggerToRestore.focus();
                }
            };

            if (immediate) {
                finalizeClose();
                return;
            }

            afterTransition(modal, finalizeClose, 300);
        };

        document.addEventListener('click', (event) => {
            const target = event.target;
            if (!(target instanceof Element)) return;

            const modalTrigger = target.closest('[data-bs-toggle="modal"][data-bs-target]');
            if (isElement(modalTrigger)) {
                const selector = modalTrigger.getAttribute('data-bs-target');
                if (!selector || !selector.startsWith('#')) return;

                const id = selector.slice(1);
                if (!MODAL_IDS.has(id)) return;

                const modal = document.getElementById(id);
                if (!isElement(modal)) return;

                event.preventDefault();
                openModal(modal, modalTrigger);
                return;
            }

            const dismissButton = target.closest('[data-bs-dismiss="modal"]');
            if (isElement(dismissButton)) {
                const modal = dismissButton.closest('.modal');
                if (!isElement(modal) || !MODAL_IDS.has(modal.id)) return;
                event.preventDefault();
                closeModal(modal);
                return;
            }

            const modalRoot = target.classList.contains('modal') ? target : null;
            if (isElement(modalRoot) && MODAL_IDS.has(modalRoot.id)) {
                closeModal(modalRoot);
            }
        });

        document.addEventListener('keydown', (event) => {
            if (!activeModal || !MODAL_IDS.has(activeModal.id)) return;

            if (event.key === 'Escape') {
                event.preventDefault();
                closeModal(activeModal);
                return;
            }

            if (event.key !== 'Tab') return;

            const focusable = getFocusable(activeModal);
            if (focusable.length === 0) return;

            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            const current = document.activeElement;

            if (event.shiftKey && current === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && current === last) {
                event.preventDefault();
                first.focus();
            }
        });
    };

    document.addEventListener('DOMContentLoaded', () => {
        setupNavbarCollapse();
        setupFaqAccordion();
        setupModals();
    });
})();
