
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Count
from django.shortcuts import get_object_or_404
from . import models


class HomeView(TemplateView):
    template_name = "home/home_site.html"

class AboutView(TemplateView):
    template_name = "about/about_site.html"

class ServicesView(TemplateView):
    template_name = "services/service_site.html"

class PlansView(TemplateView):
    template_name = "plans/plans_site.html"


from django.db.models import Count

class BlogListView(ListView):
    model = models.BlogPost
    template_name = 'blog/blog_site.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ('-updated_at',)

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True).prefetch_related('tags')

        tag_name = self.request.GET.get('tag')
        if tag_name:
            qs = qs.filter(tags__name=tag_name)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tags'] = models.Tag.objects.annotate(
            total_posts=Count('blog_posts')
        ).order_by('name')

        context['active_tag'] = self.request.GET.get('tag', '')

        context['full_posts'] = models.BlogPost.objects.filter(is_active=True).count()

        return context


class BlogDetailView(DetailView):
    model = models.BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        return get_object_or_404(models.BlogPost, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sidebar (igual lista)
        context['tags'] = models.Tag.objects.annotate(
            total_posts=Count('blog_posts')
        ).order_by('name')

        # relacionados (opcional, simples)
        post = context['post']
        context['related_posts'] = (
            models.BlogPost.objects.filter(is_active=True, tags__in=post.tags.all())
            .exclude(pk=post.pk)
            .distinct()
            .order_by('-updated_at')[:3]
        )


        return context

class ContactView(TemplateView):
    template_name = "contact/contact_site.html"
