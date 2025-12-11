document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.blog-filter-btn');
    const blogCards = document.querySelectorAll('.blog-card');

    filterButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const filter = this.getAttribute('data-filter');

            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            blogCards.forEach(function (card) {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    card.parentElement.classList.remove('d-none');
                } else {
                    card.parentElement.classList.add('d-none');
                }
            });
        });
    });
});
