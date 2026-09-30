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

    if (header && navigation) {
        const sectionLinks = [...navigation.querySelectorAll('.lp-header__links a[href^="#"]')]
            .map((link) => ({ link, section: document.getElementById(link.hash.slice(1)) }))
            .filter(({ section }) => section);

        if (sectionLinks.length) {
            let navigationFrame = null;
            const updateActiveSection = () => {
                navigationFrame = null;
                const marker = header.getBoundingClientRect().height + Math.min(window.innerHeight * 0.2, 160);
                const active = sectionLinks.find(({ section }) => {
                    const bounds = section.getBoundingClientRect();
                    return bounds.top <= marker && bounds.bottom > marker;
                });

                sectionLinks.forEach(({ link }) => {
                    if (link === active?.link) link.setAttribute('aria-current', 'location');
                    else link.removeAttribute('aria-current');
                });
            };

            const scheduleActiveSection = () => {
                if (navigationFrame !== null) return;
                navigationFrame = window.requestAnimationFrame(updateActiveSection);
            };

            updateActiveSection();
            window.addEventListener('scroll', scheduleActiveSection, { passive: true });
            window.addEventListener('resize', scheduleActiveSection);
            window.addEventListener('pageshow', scheduleActiveSection);
        }
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

    if (window.AOS && !reducedMotionQuery.matches) {
        const revealTargets = [
            '.tax-help__intro', '.tax-help__entry',
            '.lp-service__intro', '.lp-service__plan',
            '.lp-about__content', '.lp-about__visual',
            '.lp-faq__intro', '.lp-faq__item',
        ];

        document.querySelectorAll(revealTargets.join(',')).forEach((element) => {
            element.setAttribute('data-aos', 'fade-up');
        });

        window.AOS.init({ duration: 650, once: true, offset: 80, easing: 'ease-out' });
    }

    const aboutStats = document.querySelector('[data-lp-about-stats]');
    if (aboutStats && !reducedMotionQuery.matches && 'IntersectionObserver' in window) {
        const numbers = [...aboutStats.querySelectorAll('[data-lp-about-count]')];
        const observer = new IntersectionObserver((entries) => {
            if (!entries.some((entry) => entry.isIntersecting)) return;
            observer.disconnect();

            const startTime = performance.now();
            const duration = 1000;
            const updateNumbers = (now) => {
                const progress = Math.min((now - startTime) / duration, 1);
                const easedProgress = 1 - Math.pow(1 - progress, 3);

                numbers.forEach((number) => {
                    const target = Number(number.dataset.lpAboutCount);
                    const prefix = number.dataset.lpAboutPrefix || '';
                    const suffix = number.dataset.lpAboutSuffix || '';
                    number.textContent = `${prefix}${Math.round(target * easedProgress)}${suffix}`;
                });

                if (progress < 1) window.requestAnimationFrame(updateNumbers);
            };

            window.requestAnimationFrame(updateNumbers);
        }, { threshold: 0.35 });

        observer.observe(aboutStats);
    }

    const reviewsSection = document.querySelector('[data-lp-reviews]');
    if (reviewsSection && !reducedMotionQuery.matches && 'IntersectionObserver' in window) {
        const reviewCards = reviewsSection.querySelectorAll('.lp-reviews__card');
        const reviewsObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                reviewsObserver.unobserve(entry.target);
            });
        }, { threshold: 0.1 });

        reviewCards.forEach((card) => reviewsObserver.observe(card));
    }

    const faqSection = document.querySelector('[data-lp-faq]');
    if (faqSection) {
        const faqItems = [...faqSection.querySelectorAll('.lp-faq__item')];

        faqItems.forEach((item) => {
            item.addEventListener('toggle', () => {
                if (item.open) {
                    faqItems.forEach((other) => {
                        if (other !== item) other.open = false;
                    });
                }
                if (window.AOS && !reducedMotionQuery.matches) {
                    window.requestAnimationFrame(() => window.AOS.refresh());
                }
            });
        });

        faqSection.addEventListener('keydown', (event) => {
            if (event.key !== 'Escape' || !(event.target instanceof Element)) return;
            const item = event.target.closest('.lp-faq__item');
            if (!item?.open) return;

            item.open = false;
            item.querySelector('summary')?.focus();
            event.preventDefault();
        });
    }

    const ctaSection = document.querySelector('[data-lp-cta]');
    if (ctaSection && !reducedMotionQuery.matches && 'IntersectionObserver' in window) {
        const ctaContent = ctaSection.querySelector('.lp-cta__content');
        if (ctaContent) {
            const ctaObserver = new IntersectionObserver((entries) => {
                if (!entries.some((entry) => entry.isIntersecting)) return;
                ctaContent.classList.add('is-visible');
                ctaObserver.disconnect();
            }, { threshold: 0.15 });

            ctaObserver.observe(ctaSection);
        }
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
