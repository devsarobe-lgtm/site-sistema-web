from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sobre/', views.AboutView.as_view(), name='about'),
    path('servicos/', views.ServicesView.as_view(), name='services'),
    path('contato/', views.ContactView.as_view(), name='contact'),
    path('atualizacao/', views.BlogListView.as_view(), name='blog'),
    path('planos/', views.PlansView.as_view(), name='plans'),
    path('atualizacao/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail')
]
