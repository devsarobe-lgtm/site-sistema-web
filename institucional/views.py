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
        context["lp_meta_title"] = (
            "Reforma Tributária na Grande Florianópolis | Sarobe Contabilidade"
        )
        context["lp_meta_description"] = (
            "Orientação sobre a Reforma Tributária para empresas de São José "
            "e Grande Florianópolis. Entenda possíveis impactos da CBS e do "
            "IBS nas rotinas fiscais."
        )
        context["lp_nav_items"] = [
            {"label": "Home", "url": "#inicio"},
            {"label": "Atuação", "url": "#como-podemos-ajudar"},
            {"label": "Serviços", "url": "#servicos"},
            {"label": "Sobre", "url": "#sobre-a-sarobe"},
            {"label": "Avaliações", "url": "#avaliacoes"},
            {"label": "Dúvidas", "url": "#perguntas-frequentes"},
        ]
        context["lp_whatsapp_url"] = (
            "https://wa.me/554832660069?text=Ol%C3%A1%21%20Gostaria%20de%20"
            "conversar%20sobre%20a%20Reforma%20Tribut%C3%A1ria."
        )
        context["lp_header_contact_label"] = "Fale com a Sarobe"
        context["lp_hero"] = {
            "id": "inicio",
            "eyebrow": "Sarobe Contabilidade | São José/SC",
            "title": "Reforma Tributária: entenda o que muda para sua empresa",
            "description": (
                "A Sarobe orienta empresas da Grande Florianópolis sobre "
                "possíveis impactos da CBS e do IBS em notas fiscais, cadastros "
                "e rotinas, conforme suas atividades e regime tributário."
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
                {"icon": "shield", "label": "Análise de impactos fiscais"},
                {"icon": "people", "label": "Orientação sobre CBS e IBS"},
                {"icon": "chart", "label": "Revisão de rotinas fiscais"},
                {"icon": "star", "label": "Acompanhamento da transição"},
            ],
        }
        context["lp_help_you"] = {
            "eyebrow": "Como podemos ajudar",
            "title": "Orientação contábil para cada etapa da transição",
            "description": (
                "A Reforma Tributária do Consumo introduz a CBS e o IBS em etapas. "
                "Avaliamos as operações e as rotinas fiscais da sua empresa para "
                "identificar pontos de atenção e orientar os próximos passos."
            ),
            "cta_label": "Conversar com a Sarobe",
            "items": [
                {
                    "icon": "diagnosis",
                    "title": "Diagnóstico das operações",
                    "description": (
                        "Analisamos atividades, operações e regime tributário para "
                        "identificar possíveis efeitos da CBS e do IBS nas rotinas fiscais."
                    ),
                    "highlights": [
                        "Mapeamento das operações",
                        "Revisão de documentos fiscais",
                        "Pontos de atenção",
                    ],
                },
                {
                    "icon": "plan",
                    "title": "Plano de adequação",
                    "description": (
                        "Definimos com sua equipe prioridades para revisar cadastros, "
                        "emissão de notas fiscais e processos de apuração."
                    ),
                    "highlights": [
                        "Prioridades de adequação",
                        "Revisão de cadastros",
                        "Etapas de implementação",
                    ],
                },
                {
                    "icon": "implementation",
                    "title": "Orientação nos ajustes",
                    "description": (
                        "Orientamos a revisão das rotinas contábeis e fiscais e "
                        "esclarecemos dúvidas da equipe durante a aplicação dos ajustes."
                    ),
                    "highlights": [
                        "Rotinas contábeis e fiscais",
                        "Documentos fiscais",
                        "Orientação à equipe",
                    ],
                },
                {
                    "icon": "monitoring",
                    "title": "Acompanhamento da transição",
                    "description": (
                        "Acompanhamos normas e comunicados oficiais para revisar "
                        "as orientações à medida que a transição avança."
                    ),
                    "highlights": [
                        "Atualizações normativas",
                        "Revisão das orientações",
                        "Próximos passos",
                    ],
                },
            ],
        }
        context["lp_faq"] = {
            "eyebrow": "Dúvidas frequentes",
            "title": "Dúvidas sobre a Reforma Tributária",
            "description": (
                "Entenda pontos da Reforma Tributária do Consumo que podem "
                "afetar a rotina fiscal da sua empresa."
            ),
            "support_text": (
                "As exigências variam conforme a atividade, as operações e o "
                "regime tributário. Converse com a equipe sobre o seu caso."
            ),
            "cta_label": "Conversar com a Sarobe",
            "items": [
                {
                    "question": "O que muda para minha empresa com a Reforma Tributária?",
                    "answer": (
                        "A Reforma Tributária do Consumo introduz gradualmente a CBS e "
                        "o IBS. Pode ser necessário revisar notas fiscais, cadastros e "
                        "apuração de tributos. Os efeitos dependem da atividade, das "
                        "operações e do regime tributário da empresa."
                    ),
                },
                {
                    "question": "Empresas do Simples Nacional também precisam se preparar?",
                    "answer": (
                        "Sim. O Simples Nacional permanece, mas as regras da CBS e do "
                        "IBS também exigem atenção às operações, aos documentos fiscais "
                        "e à forma de recolhimento aplicável. A análise deve considerar "
                        "a realidade de cada empresa."
                    ),
                },
                {
                    "question": "Por onde começar a preparação para a Reforma Tributária?",
                    "answer": (
                        "Comece pelas atividades e operações da empresa, pelo regime "
                        "tributário, pelos cadastros e pelos documentos fiscais emitidos. "
                        "Com essas informações, é possível identificar pontos de "
                        "atenção e organizar as prioridades de revisão."
                    ),
                },
                {
                    "question": "Como a Sarobe pode orientar minha empresa nessa transição?",
                    "answer": (
                        "A equipe avalia as rotinas fiscais e os documentos da empresa, "
                        "indica prioridades de adequação e orienta os ajustes conforme "
                        "as exigências aplicáveis. O acompanhamento considera a evolução "
                        "das normas durante a transição."
                    ),
                },
                {
                    "question": "Quanto tempo leva para adequar minha empresa?",
                    "answer": (
                        "O prazo varia conforme as operações, os sistemas e os "
                        "documentos fiscais utilizados. Após analisar esse cenário "
                        "e o cronograma aplicável, é possível planejar a adequação "
                        "por etapas, sem presumir um prazo único para todas as empresas."
                    ),
                },
            ],
        }
        context["lp_cta"] = {
            "eyebrow": "Orientação para sua empresa",
            "title": "Converse sobre a Reforma Tributária",
            "description": (
                "Converse com a Sarobe sobre a CBS, o IBS e os possíveis ajustes "
                "em documentos e rotinas fiscais. A orientação considera as "
                "atividades, as operações e o regime tributário da sua empresa."
            ),
            "benefits": [
                {"icon": "shield", "label": "Análise das operações"},
                {"icon": "chart", "label": "Orientação sobre rotinas fiscais"},
                {"icon": "people", "label": "Acompanhamento da transição"},
            ],
            "image_path": "img/lp/cta-office.webp",
            "primary_label": "Conversar com a Sarobe",
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
        }
        return context
