"""
Products API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.products.api import views

router = routers.DefaultRouter()
router.register(r'designs', views.ProductDesignView)

app_name = "product"
urlpatterns = [
    re_path(r'^', include(router.urls)),
]
