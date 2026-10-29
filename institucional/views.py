from urllib.parse import urlencode

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

class OnlineAccountingView(TemplateView):
    template_name = "lp/online_accounting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lp_meta_title"] = (
            "Trocar de contabilidade online em São José | Sarobe"
        )
        context["lp_meta_description"] = (
            "Cansado de cobranças extras e robôs? Troque de contabilidade online "
            "com atendimento humano e custos claros em São José e Grande Florianópolis. "
            "Conheça a Sarobe."
        )
        context["lp_nav_items"] = [
            {"label": "Início", "url": "#inicio"},
            {"label": "O que muda", "url": "#como-podemos-ajudar"},
            {"label": "Como trocar", "url": "#como-trocar-de-contabilidade"},
            {"label": "Serviços", "url": "#servicos"},
            {"label": "Sobre", "url": "#sobre-a-sarobe"},
            {"label": "Avaliações", "url": "#avaliacoes"},
            {"label": "Dúvidas", "url": "#perguntas-frequentes"},
        ]
        context["lp_whatsapp_url"] = "https://wa.me/554832660069?" + urlencode({
            "text": "Olá! Quero trocar de contabilidade online e conhecer "
            "o atendimento e a proposta da Sarobe para o meu CNPJ."
        })
        context["lp_header_contact_label"] = "Fale com nossa equipe"
        context["lp_hero"] = {
            "id": "inicio",
            "eyebrow": "Contabilidade com atendimento humano | São José/SC",
            "title": "Cansado da contabilidade online que complica o seu CNPJ?",
            "description": (
                "Cobranças extras, respostas de robô e o mesmo problema a cada "
                "contato? Na Sarobe, você fala com pessoas, entende os custos "
                "e tem acompanhamento próximo do seu CNPJ."
            ),
            "primary_label": "Quero trocar de contador",
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
            "secondary_label": "Conhecer o atendimento",
            "secondary_url": "#como-podemos-ajudar",
            "image_path": "img/team/team_home.webp",
            "image_alt": "Equipe da Sarobe Contabilidade, em São José, SC",
            "image_width": 500,
            "image_height": 333,
            "benefits": [
                {"icon": "shield", "label": "Clareza sobre custos e serviços"},
                {"icon": "people", "label": "Atendimento com pessoas"},
                {"icon": "chart", "label": "Acompanhamento das demandas"},
                {"icon": "star", "label": "Continuidade no atendimento"},
            ],
        }
        context["lp_help_you"] = {
            "eyebrow": "Sua empresa merece ser ouvida",
            "title": "Menos desgaste com a contabilidade. Mais clareza para decidir.",
            "description": (
                "Se você está insatisfeito com a contabilidade online, compare "
                "mais do que a mensalidade. Na Sarobe, em São José e na Grande "
                "Florianópolis, a conversa inclui custos, canais de atendimento "
                "e como suas demandas serão acompanhadas."
            ),
            "cta_label": "Quero conversar com a equipe",
            "note": (
                "Alterações de CNPJ e serviços fora do escopo podem ter custos "
                "específicos. Alinhe o que está incluído e o que exige orçamento "
                "antes de contratar."
            ),
            "items": [
                {
                    "icon": "plan",
                    "title": "Mensalidade baixa, mas tudo custa à parte?",
                    "description": (
                        "Entenda o escopo da proposta antes de decidir. Conversamos "
                        "sobre a rotina do seu CNPJ, os serviços incluídos e as "
                        "situações que precisam de orçamento separado."
                    ),
                    "highlights": [
                        "Serviços incluídos na proposta",
                        "Alterações cadastrais com escopo definido",
                        "Custos extras alinhados previamente",
                    ],
                },
                {
                    "icon": "people",
                    "title": "Precisa de orientação e só recebe respostas de robô?",
                    "description": (
                        "Converse com a equipe da Sarobe sobre a realidade da sua "
                        "empresa. O atendimento humano ajuda a entender a dúvida "
                        "e orientar o próximo passo com uma linguagem clara."
                    ),
                    "highlights": [
                        "Contato com a equipe pelo WhatsApp",
                        "Orientação para o seu caso",
                        "Explicações em linguagem clara",
                    ],
                },
                {
                    "icon": "monitoring",
                    "title": "Seu problema fica parado sem uma resposta clara?",
                    "description": (
                        "Organizamos as demandas com você e alinhamos prioridades, "
                        "documentos necessários e próximos passos. O prazo considera "
                        "a complexidade do caso e eventuais dependências externas."
                    ),
                    "highlights": [
                        "Prioridades alinhadas",
                        "Próximos passos definidos",
                        "Acompanhamento das pendências",
                    ],
                },
                {
                    "icon": "conversation",
                    "title": "Troca o atendente e você precisa contar tudo de novo?",
                    "description": (
                        "Acompanhamos o contexto da sua empresa para dar continuidade "
                        "às orientações. Você conversa com uma equipe que conhece "
                        "a demanda e considera o que já foi tratado."
                    ),
                    "highlights": [
                        "Contexto da empresa considerado",
                        "Continuidade nas orientações",
                        "Equipe próxima do seu negócio",
                    ],
                },
            ],
        }
        context["lp_migration"] = {
            "eyebrow": "Troca de contador com planejamento",
            "title": "Trocar de contabilidade pode ser mais simples.",
            "description": (
                "A Sarobe avalia a rotina do seu CNPJ, apresenta uma proposta "
                "clara e orienta a transição, considerando documentos, "
                "pendências e prazos."
            ),
            "steps": [
                {
                    "icon": "document",
                    "title": "Conte o que precisa mudar",
                    "description": (
                        "Compartilhe sua atividade, o regime tributário e as "
                        "dificuldades com custos, atendimento ou pendências."
                    ),
                },
                {
                    "icon": "analysis",
                    "title": "Compare uma proposta clara",
                    "description": (
                        "Confira a mensalidade, os serviços incluídos, os custos "
                        "de demandas extras e como será o atendimento."
                    ),
                },
                {
                    "icon": "transition",
                    "title": "Organize a transição com a equipe",
                    "description": (
                        "Alinhe os documentos e as responsabilidades de cada "
                        "escritório antes de definir o início do acompanhamento."
                    ),
                },
            ],
            "cta_label": "Conversar sobre minha troca de contador",
        }
        context["lp_faq"] = {
            "eyebrow": "Respostas para decidir com clareza",
            "title": "Dúvidas sobre trocar de contabilidade online",
            "description": (
                "Veja o que avaliar sobre cobranças extras, atendimento humano "
                "e continuidade antes de escolher outro escritório contábil."
            ),
            "support_text": (
                "Cada CNPJ tem uma rotina. Converse com a equipe para alinhar "
                "escopo, valores e condições de atendimento para sua empresa."
            ),
            "cta_label": "Tirar dúvidas com a equipe",
            "items": [
                {
                    "question": "O que avaliar antes de trocar de contabilidade online?",
                    "answer": (
                        "Compare o escopo do contrato, o custo total e a forma de "
                        "atendimento. Confira quais serviços estão na mensalidade, "
                        "o que exige orçamento separado e como a equipe acompanha "
                        "as demandas. Na Sarobe, essa conversa orienta a proposta "
                        "para o seu CNPJ."
                    ),
                },
                {
                    "question": "Alterações no CNPJ estão incluídas na mensalidade?",
                    "answer": (
                        "Depende do escopo contratado e da alteração solicitada. "
                        "Mudanças de endereço, atividades ou quadro societário "
                        "podem exigir serviços específicos e taxas de órgãos "
                        "públicos. Na proposta da Sarobe, alinhe o que está incluído "
                        "e o que precisa de orçamento antes de autorizar o serviço."
                    ),
                },
                {
                    "question": "Na Sarobe vou falar com pessoas ou apenas com robôs?",
                    "answer": (
                        "Você pode conversar com a equipe da Sarobe pelo WhatsApp. "
                        "O atendimento humano considera sua atividade, suas dúvidas "
                        "e a rotina da empresa para orientar os próximos passos. "
                        "Os canais e as condições de atendimento são alinhados "
                        "na contratação."
                    ),
                },
                {
                    "question": "Vou falar sempre com o mesmo atendente?",
                    "answer": (
                        "O atendimento é feito pela equipe da Sarobe, com "
                        "continuidade no acompanhamento da empresa. Isso não "
                        "significa que todos os contatos serão com a mesma pessoa. "
                        "O objetivo é considerar o contexto e o que já foi tratado "
                        "para dar sequência à sua demanda."
                    ),
                },
                {
                    "question": "Qual é o prazo para resolver uma pendência contábil?",
                    "answer": (
                        "O prazo depende do tipo de pendência, dos documentos "
                        "disponíveis e de eventuais respostas de órgãos públicos "
                        "ou terceiros. A equipe avalia o caso com você para alinhar "
                        "prioridades e próximos passos, sem prometer um prazo "
                        "único para todas as situações."
                    ),
                },
                {
                    "question": "Como começo a troca para a Sarobe e quanto custa?",
                    "answer": (
                        "Entre em contato pelo WhatsApp e informe sua atividade, "
                        "o regime tributário e as necessidades da empresa. A equipe "
                        "avalia o cenário e apresenta uma proposta com escopo e "
                        "valores. A organização da transição considera documentos, "
                        "pendências e condições do contrato com o escritório atual."
                    ),
                },
                {
                    "question": "A Sarobe atende empresas de São José e da Grande Florianópolis?",
                    "answer": (
                        "Sim. A Sarobe Contabilidade está na Rua Victor Meirelles, "
                        "07, no bairro Campinas, em São José, SC, e atende empresas "
                        "da Grande Florianópolis. Para conversar sobre a troca de "
                        "contador e o atendimento da sua empresa, entre em contato "
                        "pelo WhatsApp (48) 3266-0069."
                    ),
                },
            ],
        }
        context["lp_cta"] = {
            "eyebrow": "Dê o próximo passo com clareza",
            "title": "Seu CNPJ precisa de atenção. Você precisa de respostas.",
            "description": (
                "Conte o que não está funcionando na sua contabilidade online. "
                "Converse com a equipe da Sarobe e conheça uma proposta com "
                "atendimento humano, escopo definido e acompanhamento da sua "
                "empresa em São José e na Grande Florianópolis."
            ),
            "benefits": [
                {"icon": "shield", "label": "Custos e escopo alinhados"},
                {"icon": "people", "label": "Conversa com a equipe"},
                {"icon": "chart", "label": "Troca de contador planejada"},
            ],
            "image_path": "img/lp/cta-office.webp",
            "primary_label": "Quero conhecer a proposta da Sarobe",
            "primary_url": context["lp_whatsapp_url"],
            "primary_external": True,
            "primary_icon": "whatsapp",
        }
        return context
