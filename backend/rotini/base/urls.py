"""
URL configuration for rotini2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import django.urls as django_urls

import files.urls as files_urls
import identity.urls

urlpatterns = [
    django_urls.path("admin/", admin.site.urls),
    django_urls.path("", django_urls.include(files_urls.urlpatterns)),
    django_urls.path("auth/", django_urls.include(identity.urls.urlpatterns)),
]
