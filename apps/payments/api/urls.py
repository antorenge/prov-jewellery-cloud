"""
Payments API urls
"""
from rest_framework import routers
from django.urls import include, re_path
from apps.payments.api import views

router = routers.DefaultRouter()
router.register(r'transfers', views.OwnershipTransferView)

app_name = "payments"

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^transfers/(?P<id>.+)/signed$',
            views.SignedTransferView.as_view(),
            name='signed_transfer_view'),

]
