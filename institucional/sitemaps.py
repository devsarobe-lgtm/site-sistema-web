from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost  


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["home", "about", "services", "contact", "plans", "blog", "tax_reform"]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_active=True).order_by("-created_at")

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)
