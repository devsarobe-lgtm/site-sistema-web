document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('blog-sidebar');
    if (!sidebar) return;

    const sidebarCol = sidebar.closest('.blog-detail-sidebar');
    const section = document.querySelector('.blog-detail-page');
    const header = document.querySelector('.main-header');
    const mainCol = document.querySelector('.blog-detail-main');

    if (!sidebarCol || !section || !mainCol) return;

    let baseSidebarWidth = null;
    let baseSidebarLeft = null;
    let stickyEnabled = false;

    function resetDesktopInline() {
        sidebar.style.position = 'static';
        sidebar.style.top = '';
        sidebar.style.bottom = '';
        sidebar.style.width = '';
        sidebar.style.maxWidth = '';
        sidebar.style.left = '';
    }

    function measureBaseMetrics() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        if (viewportWidth < 992) {
            baseSidebarWidth = null;
            baseSidebarLeft = null;
            return;
        }

        // mede em estado normal (static) pra pegar width + left corretos com gutter do bootstrap
        const prev = {
            position: sidebar.style.position,
            top: sidebar.style.top,
            bottom: sidebar.style.bottom,
            width: sidebar.style.width,
            maxWidth: sidebar.style.maxWidth,
            left: sidebar.style.left,
        };

        resetDesktopInline();

        const rect = sidebar.getBoundingClientRect();
        baseSidebarWidth = rect.width;
        baseSidebarLeft = rect.left;

        sidebar.style.position = prev.position;
        sidebar.style.top = prev.top;
        sidebar.style.bottom = prev.bottom;
        sidebar.style.width = prev.width;
        sidebar.style.maxWidth = prev.maxWidth;
        sidebar.style.left = prev.left;
    }

    function computeStickyEnabled() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        if (viewportWidth < 992) return false;

        resetDesktopInline();

        const headerHeight = header ? header.offsetHeight : 0;
        const gapTop = 16;
        const gapBottom = 24;

        const scrollY = window.scrollY || window.pageYOffset;

        const sidebarHeight = sidebar.offsetHeight;

        const sidebarColRect = sidebarCol.getBoundingClientRect();
        const sidebarColTopDoc = sidebarColRect.top + scrollY;

        const sectionRect = section.getBoundingClientRect();
        const bottomLimitDoc = sectionRect.bottom + scrollY - gapBottom;

        const startScroll = sidebarColTopDoc - headerHeight - gapTop;
        const endScroll = bottomLimitDoc - sidebarHeight - headerHeight - gapTop;

        const minScrollRoom = 48;
        if (endScroll <= startScroll + minScrollRoom) return false;

        // sidebar maior que o conteúdo => não ativa
        if (sidebarHeight >= mainCol.offsetHeight - 24) return false;

        return true;
    }

    function handleSidebarScroll() {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

        if (viewportWidth < 992) {
            resetDesktopInline();
            return;
        }

        if (!stickyEnabled) {
            resetDesktopInline();
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const headerHeight = header ? header.offsetHeight : 0;
        const gapTop = 16;
        const gapBottom = 0;

        const sidebarHeight = sidebar.offsetHeight;

        const sidebarColRect = sidebarCol.getBoundingClientRect();
        const sidebarColTopDoc = sidebarColRect.top + scrollY;

        const mainRect = mainCol.getBoundingClientRect();
        const bottomLimitDoc = mainRect.bottom + scrollY - gapBottom;

        const startScroll = sidebarColTopDoc - headerHeight - gapTop;
        const endScroll = bottomLimitDoc - sidebarHeight - headerHeight - gapTop;

        // trava largura natural
        const safeWidth = Math.floor((baseSidebarWidth || sidebar.getBoundingClientRect().width) * 1000) / 1000;
        sidebar.style.width = safeWidth + 'px';
        sidebar.style.maxWidth = safeWidth + 'px';

        if (scrollY <= startScroll) {
            resetDesktopInline();
            return;
        }

        if (scrollY >= endScroll) {
            sidebar.style.position = 'absolute';
            sidebar.style.left = '';
            const topAbs = bottomLimitDoc - sidebarHeight - sidebarColTopDoc;
            sidebar.style.top = topAbs + 'px';
            sidebar.style.bottom = '';
            return;
        }

        sidebar.style.position = 'fixed';
        sidebar.style.top = (headerHeight + gapTop) + 'px';
        sidebar.style.bottom = '';

        if (baseSidebarLeft != null) {
            sidebar.style.left = baseSidebarLeft + 'px';
        } else {
            sidebar.style.left = sidebar.getBoundingClientRect().left + 'px';
        }
    }

    function recomputeAll() {
        measureBaseMetrics();
        stickyEnabled = computeStickyEnabled();
        handleSidebarScroll();
    }

    recomputeAll();

    window.addEventListener('scroll', handleSidebarScroll, { passive: true });
    window.addEventListener('resize', recomputeAll);
});
