"""
Inventory API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.inventory.api import views

router = routers.DefaultRouter()
router.register(r'inventory', views.InventoryItemView)

app_name = "inventory"

urlpatterns = [
    re_path(r'^', include(router.urls)),

]
