from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from institucional.sitemaps import StaticViewSitemap, BlogPostSitemap


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogPostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('institucional.urls')),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
