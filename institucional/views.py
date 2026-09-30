from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import get_object_or_404
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
            {"label": "Atuação", "url": "#como-podemos-ajudar"},
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
            "secondary_url": "#servicos",
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
        context["lp_help_you"] = {
            "eyebrow": "Como podemos ajudar",
            "title": "Sua empresa preparada para cada etapa da transição",
            "description": (
                "A Reforma Tributária do Consumo traz novas regras para as rotinas fiscais. "
                "A Sarobe ajuda você a entender o que merece atenção e a organizar os "
                "próximos passos de acordo com a realidade do seu negócio."
            ),
            "cta_label": "Conversar com a Sarobe",
            "items": [
                {
                    "icon": "diagnosis",
                    "title": "Diagnóstico do seu negócio",
                    "description": (
                        "Analisamos suas atividades, operações e regime tributário para "
                        "identificar onde as mudanças podem afetar a empresa."
                    ),
                    "highlights": [
                        "Mapeamento de riscos",
                        "Revisão de processos",
                        "Levantamento de oportunidades",
                    ],
                },
                {
                    "icon": "plan",
                    "title": "Plano de adequação",
                    "description": (
                        "Organizamos prioridades para revisar processos, cadastros e "
                        "documentos fiscais junto com a sua equipe."
                    ),
                    "highlights": [
                        "Prioridades de ajuste",
                        "Plano por etapas",
                        "Alinhamento com a equipe",
                    ],
                },
                {
                    "icon": "implementation",
                    "title": "Apoio na implementação",
                    "description": (
                        "Acompanhamos os ajustes nas rotinas contábeis e fiscais e "
                        "orientamos as pessoas envolvidas no dia a dia."
                    ),
                    "highlights": [
                        "Revisão de cadastros",
                        "Ajustes em documentos",
                        "Orientação operacional",
                    ],
                },
                {
                    "icon": "monitoring",
                    "title": "Acompanhamento contínuo",
                    "description": (
                        "Monitoramos a regulamentação e atualizamos as orientações "
                        "conforme novas regras forem detalhadas."
                    ),
                    "highlights": [
                        "Atualizações normativas",
                        "Revisão periódica",
                        "Ajustes de rota",
                    ],
                },
            ],
        }
        context["lp_faq"] = {
            "eyebrow": "Dúvidas frequentes",
            "title": "Perguntas mais comuns",
            "description": (
                "Reunimos as principais dúvidas para você entender como a Sarobe "
                "pode apoiar sua empresa na Reforma Tributária."
            ),
            "support_text": (
                "Se ainda tiver alguma dúvida, nossa equipe está à disposição "
                "para conversar e entender a realidade do seu negócio."
            ),
            "cta_label": "Conversar com a Sarobe",
            "items": [
                {
                    "question": "Como a Reforma Tributária vai impactar minha empresa?",
                    "answer": (
                        "A Reforma Tributária do Consumo muda regras de tributação e exige "
                        "atenção aos documentos fiscais, à apuração e às obrigações "
                        "acessórias. Os efeitos variam conforme atividade, operações e "
                        "regime tributário. Nossa equipe analisa o cenário da sua empresa "
                        "para identificar as rotinas que precisam de revisão."
                    ),
                },
                {
                    "question": "Quais empresas precisam se preparar agora?",
                    "answer": (
                        "Empresas que vendem bens ou prestam serviços devem acompanhar "
                        "as exigências e o cronograma aplicáveis às suas operações e ao "
                        "seu regime tributário. O primeiro passo é revisar documentos "
                        "fiscais, cadastros e processos para definir prioridades."
                    ),
                },
                {
                    "question": "A Sarobe também ajuda na implementação das mudanças?",
                    "answer": (
                        "Sim. Além do diagnóstico, apoiamos a organização dos ajustes "
                        "nas rotinas contábeis e fiscais, orientamos sua equipe e "
                        "acompanhamos as mudanças conforme as regras forem detalhadas."
                    ),
                },
                {
                    "question": "Quanto tempo leva para minha empresa estar em conformidade?",
                    "answer": (
                        "Não existe um prazo igual para todas as empresas. O tempo "
                        "depende das operações, dos sistemas, dos cadastros e das "
                        "obrigações aplicáveis. Após avaliar sua situação, organizamos "
                        "um plano de adequação por etapas."
                    ),
                },
                {
                    "question": "Como funciona a consultoria da Sarobe?",
                    "answer": (
                        "Começamos entendendo suas atividades e rotinas fiscais. Com "
                        "base nesse diagnóstico, apresentamos prioridades, orientamos "
                        "os próximos passos e acompanhamos a implementação conforme "
                        "as necessidades da sua empresa."
                    ),
                },
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
