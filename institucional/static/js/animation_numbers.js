document.addEventListener('DOMContentLoaded', function () {
    const counters = document.querySelectorAll('.about-metric-number[data-count-target]');
    if (!('IntersectionObserver' in window)) return;

    const animateCounter = (el) => {
        const target = parseInt(el.getAttribute('data-count-target'), 10) || 0;
        const suffix = el.getAttribute('data-count-suffix') || '';
        const duration = 1200;
        const startTime = performance.now();

        const step = (now) => {
            const progress = Math.min((now - startTime) / duration, 1);
            const current = Math.floor(progress * target);
            el.textContent = current + suffix;
            if (progress < 1) requestAnimationFrame(step);
        };

        requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const el = entry.target;
                if (el.dataset.countStarted === 'true') return;
                el.dataset.countStarted = 'true';
                animateCounter(el);
            }
        });
    }, { threshold: 0.4 });

    counters.forEach((el) => observer.observe(el));
});
