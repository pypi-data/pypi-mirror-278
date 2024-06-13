from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from django_utilsds import views as utilsds_views
from django_postds.sitemaps import BlogPostSitemap, PortfolioSitemap
from .sitemaps import StaticViewSitemap
from _data import herobizdental

app_name = herobizdental.context['template_name']

sitemaps = {
    "posts": BlogPostSitemap,
    "portfolios": PortfolioSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', utilsds_views.robots),
    path('', views.home, name='home'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path('terms_of_use/', views.terms, name='terms'),
    path('privacy_policy/', views.privacy, name='privacy'),
]
