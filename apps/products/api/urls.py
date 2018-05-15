"""
Products API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.products.api import views

router = routers.DefaultRouter()
router.register(r'designs', views.ProductDesignView)
router.register(r'materials', views.MaterialView)

app_name = "products"

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^signed/(?P<sku>.+)$',
            views.SignedProductDesignView.as_view(), name='signed_view'),
    re_path(r'^validate$',
            views.ValidateJWTView.as_view(), name='validate_view'),

]
