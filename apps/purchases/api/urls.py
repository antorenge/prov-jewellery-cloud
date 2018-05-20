"""
Purchases API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.purchases.api import views

router = routers.DefaultRouter()
router.register(r'productions', views.ArtisanProductionView)
router.register(r'deliveries', views.PurchaseOrderDeliveryView)

app_name = "purchases"

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^deliveries/(?P<id>.+)/signed$',
            views.SignedDeliveryView.as_view(), name='signed_delivery_view'),

]
