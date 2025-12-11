from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/home_site.html"

class AboutView(TemplateView):
    template_name = "about/about_site.html"

class ServicesView(TemplateView):
    template_name = "services/service_site.html"

class ContactView(TemplateView):
    template_name = "contact/contact_site.html"
