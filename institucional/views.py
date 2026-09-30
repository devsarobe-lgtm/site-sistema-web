from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from . import models


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)

def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)


class HomeView(TemplateView):
    template_name = "home/home_site.html"

class AboutView(TemplateView):
    template_name = "about/about_site.html"

class ServicesView(TemplateView):
    template_name = "services/service_site.html"

class PlansView(TemplateView):
    template_name = "plans/plans_site.html"


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

class TaxReformView(TemplateView):
    template_name = "lp/tax_reform.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lp_meta_title"] = "Reforma Tributária para empresas | Sarobe Contabilidade"
        context["lp_meta_description"] = (
            "Entenda como a Reforma Tributária pode afetar sua empresa e converse "
            "com a equipe da Sarobe Contabilidade em São José/SC."
        )
        context["lp_nav_items"] = [
            {"label": "Home", "url": "#inicio"},
        ]
        context["lp_whatsapp_url"] = (
            "https://wa.me/554832660069?text=Ol%C3%A1%21%20Gostaria%20de%20"
            "conversar%20sobre%20a%20Reforma%20Tribut%C3%A1ria."
        )
        context["lp_header_contact_label"] = "Fale com a Sarobe"
        context["lp_hero"] = {
            "id": "inicio",
            "eyebrow": "Sarobe Contabilidade",
            "title": "Reforma Tributária: prepare sua empresa para as mudanças",
            "description": (
                "Conte com orientação contábil para entender os impactos "
                "da Reforma Tributária no seu negócio."
            ),
            "primary_label": "Conversar com a Sarobe",
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
            "secondary_label": "Conheça nossos serviços",
            "secondary_url": reverse("services"),
            "image_path": "img/team/team_home.webp",
            "image_alt": "Equipe da Sarobe Contabilidade reunida",
            "image_width": 500,
            "image_height": 333,
            "benefits": [
                {"icon": "shield", "label": "Segurança tributária"},
                {"icon": "people", "label": "Assessoria completa"},
                {"icon": "chart", "label": "Gestão financeira mais eficiente"},
                {"icon": "star", "label": "Atendimento personalizado"},
            ],
        }
        context["lp_cta"] = {
            "eyebrow": "Entre em contato",
            "title": "Vamos conversar sobre sua empresa?",
            "description": (
                "Nossa equipe pode ajudar você a entender o cenário "
                "tributário do seu negócio."
            ),
            "primary_label": "Falar pelo WhatsApp",
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
        }
        return context
