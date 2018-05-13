"""prov_jewellery_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, re_path
from rest_framework_swagger.views import get_swagger_view

SCHEMA_VIEW = get_swagger_view(title='API Documentation')

urlpatterns = [
    re_path(r'^docs/$', SCHEMA_VIEW),
    re_path(r'^products/', include(('apps.products.api.urls', 'products-api'),
                                   namespace='products-api')),
    re_path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls'))
]
