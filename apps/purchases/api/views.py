"""
Purchases API views
"""
import jwt
from rest_framework import viewsets, generics
from rest_framework.response import Response
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


class SignedDeliveryView(generics.RetrieveAPIView):
    """Return digitally signed purchase order delivery"""
    queryset = PurchaseOrderDelivery.objects.all()
    serializer_class = PurchaseOrderDeliverySerializer

    def get_object(self, id):
        return PurchaseOrderDelivery.objects.filter(pk=id).first()

    def get(self, request, id):
        serializer = self.get_serializer(self.get_object(id))
        encoded = jwt.encode(serializer.data, 'SECRET', algorithm='HS256')
        return Response({'id': id, 'signed': encoded})
