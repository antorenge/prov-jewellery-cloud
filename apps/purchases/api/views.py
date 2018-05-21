"""
Purchases API views
"""
import jwt
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from ..models import ArtisanProduction, PurchaseOrderDelivery
from .serializers import (ArtisanProductionSerializer,
                          PurchaseOrderDeliverySerializer, ValidateSerializer)


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


class ValidateSignedView(generics.CreateAPIView):
    """Validate signed objects"""
    serializer_class = ValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = ValidateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                signed = bytes(serializer.data['signed'], 'utf-8')
                jwt.decode(signed, 'SECRET', algorithms='HS256')
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except jwt.InvalidSignatureError as error:
                return Response({'error': str(error)},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
