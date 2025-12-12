document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('blog-sidebar');
    if (!sidebar) return;

    const sidebarCol = sidebar.closest('.blog-sidebar-column');
    const section = document.querySelector('.blog-list-section');
    const pagination = document.querySelector('.blog-pagination-nav');
    const header = document.querySelector('.main-header');

    if (!sidebarCol || !section) return;

    function handleSidebarScroll() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        // Mobile: sidebar normal, sem efeito
        if (viewportWidth < 992) {
            sidebar.style.position = 'static';
            sidebar.style.top = '';
            sidebar.style.bottom = '';
            sidebar.style.width = '';
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const headerHeight = header ? header.offsetHeight : 0;
        const gapTop = 16;       // espaço entre header e sidebar
        const gapBottom = 75;    // espaço acima da paginação

        const sidebarHeight = sidebar.offsetHeight;

        // coordenadas absolutas (na página)
        const sidebarColRect = sidebarCol.getBoundingClientRect();
        const sidebarColTopDoc = sidebarColRect.top + scrollY;

        // limite inferior: topo da paginação (se existir),
        // senão o fim da seção de blog
        let bottomLimitDoc;
        if (pagination) {
            const pagRect = pagination.getBoundingClientRect();
            bottomLimitDoc = pagRect.top + scrollY - gapBottom;
        } else {
            const sectionRect = section.getBoundingClientRect();
            bottomLimitDoc = sectionRect.top + scrollY + section.offsetHeight - gapBottom;
        }

        // ponto onde começa a “grudar”
        const startScroll = sidebarColTopDoc - headerHeight - gapTop;

        // ponto onde deve parar de seguir (antes da paginação)
        const endScroll = bottomLimitDoc - sidebarHeight - headerHeight - gapTop;

        // largura fixa quando fixed/absolute para não “pular”
        const colWidth = sidebarColRect.width;
        sidebar.style.width = colWidth + 'px';

        // Antes da área de sticky: comportamento normal
        if (scrollY <= startScroll) {
            sidebar.style.position = 'static';
            sidebar.style.top = '';
            sidebar.style.bottom = '';
            sidebar.style.width = '';
            return;
        }

        // Depois do fim: cola acima da paginação (posição absoluta dentro da coluna)
        if (scrollY >= endScroll) {
            sidebar.style.position = 'absolute';
            const topAbs = bottomLimitDoc - sidebarHeight - sidebarColTopDoc;
            sidebar.style.top = topAbs + 'px';
            sidebar.style.bottom = '';
            return;
        }

        // No meio: segue o scroll, fixo abaixo do header
        sidebar.style.position = 'fixed';
        sidebar.style.top = (headerHeight + gapTop) + 'px';
        sidebar.style.bottom = '';
    }

    window.addEventListener('scroll', handleSidebarScroll);
    window.addEventListener('resize', handleSidebarScroll);
    handleSidebarScroll();
});
