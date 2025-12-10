document.addEventListener('DOMContentLoaded', function () {
    const metricsBox = document.querySelector('.about-metrics');
    if (!metricsBox) return;

    const counters = metricsBox.querySelectorAll('.about-metric-number');
    let countersAnimated = false;

    function animateCounter(element) {
        const target = parseInt(element.dataset.target, 10);
        const duration = 1200; // ms
        const startTime = performance.now();

        function update(now) {
            const progress = Math.min((now - startTime) / duration, 1);
            const current = Math.floor(progress * target);

            if (element.textContent.includes('+')) {
                element.textContent = current + '+';
            } else if (element.textContent.includes('%')) {
                element.textContent = current + '%';
            } else {
                element.textContent = current;
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersAnimated) {
                counters.forEach(animateCounter);
                countersAnimated = true;
                observer.unobserve(metricsBox);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px 0px -10% 0px'
    });

    observer.observe(metricsBox);
});