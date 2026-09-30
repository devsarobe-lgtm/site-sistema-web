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
        context["lp_brand_url"] = "#home"
        whatsapp_message = _(
            "Olá! Encontrei a página de Reforma Tributária e gostaria de informações sobre atendimento."
        )
        context["lp_whatsapp_url"] = (
            f"https://wa.me/5548988366235?text={quote(str(whatsapp_message))}"
        )
        context["lp_hero"] = {
            "eyebrow": _("Direito Bancário · São José / SC"),
            "title": _("Direito bancário: contratos, cobranças e financiamentos"),
            "description": _("Informações sobre revisão de contratos, busca e apreensão, execuções bancárias e negociação de dívidas. Cada situação exige análise individual."),
            "primary_label": _("Contato com o advogado"),
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
            "secondary_label": _("Ver temas de atuação"),
            "secondary_url": "#atuacao",
            "highlights": [
                {"icon": "person", "title": _("Atendimento direto"), "detail": _("com o advogado")},
                {"icon": "shield", "title": _("Análise individual"), "detail": _("de cada situação")},
                {"icon": "scale", "title": _("OAB/SC 74.996"), "detail": _("Regularmente inscrito")},
            ],
        }
        context["lp_nav_items"] = [
            {"label": _("Home"), "url": "#home"},
            {"label": _("Atuação"), "url": "#atuacao"},
            {"label": _("Calculadora"), "url": "#calculadora"},
            {"label": _("Sobre"), "url": "#sobre"},
            {"label": _("Avaliações"), "url": "#avaliacoes"},
            {"label": _("FAQ"), "url": "#faq"},
        ]
        context["lp_meta_description"] = _(
            "Direito bancário em São José/SC: informações sobre contratos, financiamentos, busca e apreensão, cobranças e renegociação de dívidas."
        )
        context["lp_meta_title"] = _("Direito Bancário em São José/SC | Jorge R. Sarobe")
        context["lp_header_contact_label"] = _("Contato")
        context["lp_header_contact_aria"] = _("Contato com o advogado pelo WhatsApp")
        context["lp_footer_heading"] = _("Informações e contato")
        context["lp_footer_contact_description"] = _(
            "Jorge R. Sarobe, OAB/SC 74.996, atende em São José/SC. Entre em contato para informações sobre a análise do seu caso."
        )
        context["lp_cta"] = {
            "eyebrow": _("Contato"),
            "title": _("Dúvidas sobre um contrato bancário?"),
            "description": _("As informações desta página são gerais. A avaliação jurídica depende dos documentos e das circunstâncias do contrato."),
            "primary_label": _("Contato pelo WhatsApp"),
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
            "note": _("Jorge R. Sarobe · OAB/SC 74.996 · São José/SC"),
        }
        context["lp_help"] = {
            "id": "atuacao",
            "eyebrow": _("Direito Bancário"),
            "title": _("Temas de atuação em Direito Bancário"),
            "description": _("A atuação depende dos documentos, da modalidade contratual e das circunstâncias de cada caso."),
            "cards": [
                {
                    "icon": "document",
                    "title": _("Revisão de empréstimos e financiamentos"),
                    "description": _("Análise de juros, encargos, CET, tarifas, seguros, capitalização e evolução da dívida."),
                    "details": [
                        _("Pode abranger financiamento de veículos, empréstimos pessoais e contratos empresariais."),
                        _("A revisão depende do contrato, do histórico de pagamentos e da análise jurídica."),
                    ],
                },
                {
                    "icon": "car",
                    "title": _("Defesa em busca e apreensão de veículos"),
                    "description": _("Atuação em ações ligadas a financiamento com alienação fiduciária."),
                    "details": [
                        _("Análise do contrato, da mora e da notificação."),
                        _("Conferência dos encargos cobrados e das circunstâncias da ação."),
                    ],
                },
                {
                    "icon": "gavel",
                    "title": _("Defesa em cobranças e execuções bancárias"),
                    "description": _("Defesa de pessoas físicas e empresas em ações de cobrança e execução."),
                    "details": [
                        _("Análise de CCB, empréstimos, capital de giro, cheque especial e outras dívidas bancárias."),
                        _("Avaliação do título, dos valores exigidos, dos prazos e das possibilidades de defesa."),
                    ],
                },
                {
                    "icon": "handshake",
                    "title": _("Negociação e renegociação de dívidas bancárias"),
                    "description": _("Análise do débito e das condições propostas para pessoas e empresas."),
                    "details": [
                        _("Atuação extrajudicial ou judicial, conforme as circunstâncias."),
                        _("Avaliação de quitação, parcelamento e revisão das condições da dívida."),
                    ],
                },
                {
                    "icon": "chart",
                    "title": _("Juros abusivos e revisão de contratos bancários"),
                    "description": _("Análise técnica das taxas e dos encargos aplicados ao contrato."),
                    "details": [
                        _("Comparação com parâmetros do Banco Central, quando juridicamente pertinentes."),
                        _("Taxa acima da média, isoladamente, não define abusividade."),
                    ],
                },
            ],
        }
        context["lp_process"] = {
            "id": "processo",
            "title": _("Como ocorre"),
            "highlight": _("a análise jurídica"),
            "description": _("A orientação considera os documentos disponíveis, a legislação e as particularidades do contrato."),
            "button_label": _("Informações de contato"),
            "button_url": context["lp_whatsapp_url"],
            "button_external": True,
            "background_image": "img/lp/process-background.webp",
            "steps": [
                {
                    "icon": "document",
                    "title": _("Você apresenta o contrato"),
                    "description": _("Relato da situação e apresentação dos documentos disponíveis."),
                },
                {
                    "icon": "search",
                    "title": _("Análise de taxas, encargos e documentos"),
                    "description": _("Exame do contrato, das cobranças e dos documentos pertinentes."),
                },
                {
                    "icon": "document",
                    "title": _("Orientação sobre caminhos possíveis"),
                    "description": _("Esclarecimento das possibilidades e dos riscos identificados."),
                },
            ],
        }
        context["lp_about"] = {
            "id": "sobre",
            "eyebrow": _("Sobre o advogado"),
            "title": _("Jorge R. Sarobe: formação e atuação em Direito Bancário"),
            "description": _(
                "Advogado inscrito na OAB/SC sob o nº 74.996, com atendimento em São José/SC. Formação em Direito Bancário documentada abaixo."
            ),
            "background_image": "img/lp/about-background.webp",
            "photo": "img/photos/jorge_com_fundo.webp",
            "photo_alt": _("Jorge R. Sarobe em seu escritório"),
            "name": "Jorge R. Sarobe",
            "registration": _("OAB/SC 74.996"),
            "credentials": [
                {
                    "icon": "graduation",
                    "title": _("Graduação em Direito"),
                    "description": _("Graduado pela Universidade Estácio de Sá (2020)"),
                },
                {
                    "icon": "book",
                    "title": _("Formação em Direito Bancário"),
                    "description": _("Pós-graduação em Direito Bancário e certificado ESA em Direito Bancário na Prática"),
                },
                {
                    "icon": "people",
                    "title": _("Atuação institucional"),
                    "description": _("Integrante da Comissão de Direito Bancário da OAB/SC — Subseção São José"),
                },
                {
                    "icon": "court",
                    "title": _("Experiência prática"),
                    "description": _("Ex-conciliador judicial no Fórum de São José/SC"),
                },
            ],
            "quote": {
                "text": _(
                    "Meu compromisso é oferecer um atendimento jurídico claro, ético e técnico, sempre com foco na análise responsável de cada caso."
                ),
                "author": "Jorge R. Sarobe",
                "registration": _("OAB/SC 74.996"),
            },
            "documents_label": _("Documentos de formação em Direito Bancário"),
            "modal_title": _("Documento de Direito Bancário"),
            "documents": [
                {
                    "path": "doc/Diploma Direito Bancário.pdf",
                    "label": _("Ver diploma de Direito Bancário"),
                    "caption": _("Visualizar PDF"),
                },
                {
                    "path": "doc/Certificado ESA Direito Bancario.pdf",
                    "label": _("Ver certificado ESA: Direito Bancário na Prática"),
                    "caption": _("Visualizar PDF"),
                },
            ],
        }
        context["lp_faq"] = {
            "id": "faq",
            "eyebrow": "FAQ",
            "title": _("Dúvidas frequentes"),
            "description": _("Respostas gerais sobre contratos, cobranças e atendimento. A análise de cada caso depende dos documentos."),
            "items": [
                {
                    "question": _("O que pode ser analisado em um contrato bancário?"),
                    "answer": _(
                        "Podem ser examinados juros, encargos, CET, tarifas, seguros, capitalização e evolução da dívida, conforme a modalidade e os documentos disponíveis. A análise não implica revisão automática do contrato."
                    ),
                },
                {
                    "question": _("Quais documentos ajudam na análise?"),
                    "answer": _(
                        "Contrato, extratos, comprovantes de pagamento, planilhas e comunicações do banco costumam ser úteis. Em processos judiciais, também são importantes a petição e as intimações recebidas."
                    ),
                },
                {
                    "question": _("Taxa acima da média do Banco Central é abusiva?"),
                    "answer": _(
                        "Não necessariamente. As séries do Banco Central são referências estatísticas, não limites legais automáticos. A avaliação jurídica considera a modalidade, a época da contratação, as cláusulas e as circunstâncias do caso."
                    ),
                    "open": True,
                },
                {
                    "question": _("O que é examinado em busca e apreensão de veículo?"),
                    "answer": _(
                        "Em financiamentos com alienação fiduciária, podem ser examinados o contrato, a mora, a notificação, os encargos cobrados e os documentos do processo. Os prazos judiciais exigem atenção individual."
                    ),
                },
                {
                    "question": _("Como funciona a defesa em cobrança ou execução bancária?"),
                    "answer": _(
                        "O advogado examina o título, a dívida exigida, os documentos e os prazos processuais. A atuação pode envolver CCB, empréstimos, capital de giro e cheque especial, conforme o caso."
                    ),
                },
                {
                    "question": _("É possível negociar uma dívida bancária?"),
                    "answer": _(
                        "Podem ser avaliadas propostas de renegociação, quitação ou parcelamento, pela via extrajudicial ou judicial. As condições dependem do contrato, do débito e da negociação com a instituição financeira."
                    ),
                },
                {
                    "question": _("Como obter informações sobre atendimento e honorários?"),
                    "answer": _(
                        "O contato pode ser feito pelo WhatsApp. As condições da consulta e dos honorários são informadas antes de eventual contratação, conforme o serviço necessário."
                    ),
                },
            ],
        }
        return context
