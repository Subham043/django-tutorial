"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from blogs.models import Article
from polls import urls as polls_url
from blogs import urls as blogs_url
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

admin.site.site_header = 'My administration'

info_dict = {
    'queryset': Article.objects.all(),
    'date_field': 'publish_on',
}

urlpatterns = [
    path('polls/', include(polls_url)),
    path('blogs/', include(blogs_url)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap,
         {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
