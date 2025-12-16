document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('blog-sidebar');
    if (!sidebar) return;

    const sidebarCol = sidebar.closest('.blog-sidebar-column');
    const section = document.querySelector('.blog-list-section');
    const pagination = document.querySelector('.blog-pagination-nav');
    const header = document.querySelector('.main-header');
    const mainCol = document.querySelector('.blog-main-column');

    if (!sidebarCol || !section || !mainCol) return;

    let baseSidebarWidth = null;
    let stickyEnabled = false;

    function resetDesktopInline() {
        sidebar.style.position = 'static';
        sidebar.style.top = '';
        sidebar.style.bottom = '';
        sidebar.style.width = '';
        sidebar.style.maxWidth = '';
    }

    function getPostCount() {
        // conta os cards do blog renderizados
        return mainCol.querySelectorAll('.blog-list-card').length;
    }

    function measureBaseSidebarWidth() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        if (viewportWidth < 992) {
            baseSidebarWidth = null;
            return;
        }

        // mede sempre em estado "normal" (static), pra não variar depois que fixa
        const prevPosition = sidebar.style.position;
        const prevTop = sidebar.style.top;
        const prevBottom = sidebar.style.bottom;
        const prevWidth = sidebar.style.width;
        const prevMaxWidth = sidebar.style.maxWidth;

        resetDesktopInline();
        baseSidebarWidth = sidebar.getBoundingClientRect().width;

        sidebar.style.position = prevPosition;
        sidebar.style.top = prevTop;
        sidebar.style.bottom = prevBottom;
        sidebar.style.width = prevWidth;
        sidebar.style.maxWidth = prevMaxWidth;
    }

    function computeStickyEnabled() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        // mobile: nunca sticky
        if (viewportWidth < 992) return false;

        // ✅ regra pedida: 1–2 posts => não ativa sticky
        const postCount = getPostCount();
        if (postCount <= 2) return false;

        // fallback: se coluna principal é curta demais (mesmo com + posts)
        // mede com sidebar em static pra não “contaminar”
        resetDesktopInline();

        const headerHeight = header ? header.offsetHeight : 0;
        const gapTop = 16;
        const gapBottom = 75;

        const scrollY = window.scrollY || window.pageYOffset;

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

        const startScroll = sidebarColTopDoc - headerHeight - gapTop;
        const endScroll = bottomLimitDoc - sidebarHeight - headerHeight - gapTop;

        // se não existe espaço real pra “andar”, não ativa
        const minScrollRoom = 48;
        if (endScroll <= startScroll + minScrollRoom) return false;

        return true;
    }

    function handleSidebarScroll() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        // mobile: normal
        if (viewportWidth < 992) {
            resetDesktopInline();
            return;
        }

        // ✅ se não é pra ativar, mantém normal SEM ficar alternando
        if (!stickyEnabled) {
            resetDesktopInline();
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

        const startScroll = sidebarColTopDoc - headerHeight - gapTop;
        const endScroll = bottomLimitDoc - sidebarHeight - headerHeight - gapTop;

        // trava na largura natural do card (constante)
        const safeWidth = Math.floor((baseSidebarWidth || sidebar.getBoundingClientRect().width) * 1000) / 1000;
        sidebar.style.width = safeWidth + 'px';
        sidebar.style.maxWidth = safeWidth + 'px';

        if (scrollY <= startScroll) {
            resetDesktopInline();
            return;
        }

        if (scrollY >= endScroll) {
            sidebar.style.position = 'absolute';
            const topAbs = bottomLimitDoc - sidebarHeight - sidebarColTopDoc;
            sidebar.style.top = topAbs + 'px';
            sidebar.style.bottom = '';
            return;
        }

        sidebar.style.position = 'fixed';
        sidebar.style.top = (headerHeight + gapTop) + 'px';
        sidebar.style.bottom = '';
    }

    function recomputeAll() {
        measureBaseSidebarWidth();
        stickyEnabled = computeStickyEnabled();
        handleSidebarScroll();
    }

    recomputeAll();

    window.addEventListener('scroll', handleSidebarScroll, { passive: true });
    window.addEventListener('resize', recomputeAll);
});
