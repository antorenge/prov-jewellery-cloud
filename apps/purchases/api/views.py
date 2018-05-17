"""
Purchases API views
"""
from rest_framework import viewsets
from ..models import ArtisanProduction, PurchaseOrderDelivery
from .serializers import (ArtisanProductionSerializer,
                          PurchaseOrderDeliverySerializer)


class ArtisanProductionView(viewsets.ModelViewSet):
    """Return artisan productions"""
    queryset = ArtisanProduction.objects.all()
    serializer_class = ArtisanProductionSerializer


class PurchaseOrderDeliveryView(viewsets.ModelViewSet):
    """Return purchase order deliveries"""
    queryset = PurchaseOrderDelivery.objects.all()
    serializer_class = PurchaseOrderDeliverySerializer
