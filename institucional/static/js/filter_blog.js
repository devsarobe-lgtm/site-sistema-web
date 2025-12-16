document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.blog-sidebar-category[data-filter]');
    if (!filterButtons.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const tag = (this.getAttribute('data-filter') || '').trim();

            const url = new URL(window.location.href);

            // sempre que trocar tag, volta pra página 1
            url.searchParams.delete('page');

            if (tag) {
                url.searchParams.set('tag', tag);
            } else {
                // "Todas"
                url.searchParams.delete('tag');
            }

            window.location.href = url.toString();
        });
    });
});
