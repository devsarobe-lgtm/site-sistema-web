document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('blog-sidebar');
    if (!sidebar) return;

    const sidebarCol = sidebar.closest('.blog-sidebar-column');
    const section = document.querySelector('.blog-list-section');
    const pagination = document.querySelector('.blog-pagination-nav');
    const header = document.querySelector('.main-header');

    if (!sidebarCol || !section) return;

    // cache da largura "natural" do card (antes de virar fixed/absolute)
    let baseSidebarWidth = null;

    function measureBaseSidebarWidth() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        // no mobile não precisa travar largura
        if (viewportWidth < 992) {
            baseSidebarWidth = null;
            return;
        }

        // limpa inline pra medir como o layout original renderiza
        const prevPosition = sidebar.style.position;
        const prevTop = sidebar.style.top;
        const prevBottom = sidebar.style.bottom;
        const prevWidth = sidebar.style.width;
        const prevMaxWidth = sidebar.style.maxWidth;

        sidebar.style.position = 'static';
        sidebar.style.top = '';
        sidebar.style.bottom = '';
        sidebar.style.width = '';
        sidebar.style.maxWidth = '';

        // width real do card no layout (pode vir com subpixel)
        baseSidebarWidth = sidebar.getBoundingClientRect().width;

        // restaura
        sidebar.style.position = prevPosition;
        sidebar.style.top = prevTop;
        sidebar.style.bottom = prevBottom;
        sidebar.style.width = prevWidth;
        sidebar.style.maxWidth = prevMaxWidth;
    }

    function handleSidebarScroll() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        // Mobile: sidebar normal, sem efeito
        if (viewportWidth < 992) {
            sidebar.style.position = 'static';
            sidebar.style.top = '';
            sidebar.style.bottom = '';
            sidebar.style.width = '';
            sidebar.style.maxWidth = '';
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const headerHeight = header ? header.offsetHeight : 0;
        const gapTop = 16;
        const gapBottom = 75;

        const sidebarHeight = sidebar.offsetHeight;

        const sidebarColRect = sidebarCol.getBoundingClientRect();
        const sidebarColTopDoc = sidebarColRect.top + scrollY;

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

        // trava na largura natural do card (não na largura da coluna)
        const safeWidth = Math.floor((baseSidebarWidth || sidebar.getBoundingClientRect().width) * 1000) / 1000;
        sidebar.style.width = safeWidth + 'px';
        sidebar.style.maxWidth = safeWidth + 'px';

        // Antes da área de sticky: comportamento normal
        if (scrollY <= startScroll) {
            sidebar.style.position = 'static';
            sidebar.style.top = '';
            sidebar.style.bottom = '';
            sidebar.style.width = '';
            sidebar.style.maxWidth = '';
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

    // mede a largura base primeiro
    measureBaseSidebarWidth();
    handleSidebarScroll();

    window.addEventListener('scroll', handleSidebarScroll);
    window.addEventListener('resize', function () {
        measureBaseSidebarWidth();
        handleSidebarScroll();
    });
});
