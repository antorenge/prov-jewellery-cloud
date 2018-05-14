"""
Products API views
"""
import jwt
from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProductDesign, Material
from .serializers import ProductDesignSerializer, MaterialSerializer


class ProductDesignView(viewsets.ModelViewSet):
    """Return a product design"""
    queryset = ProductDesign.objects.all()
    serializer_class = ProductDesignSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)

    search_fields = ('sku', 'name')
    ordering_fields = ('date_created',)


class MaterialView(viewsets.ModelViewSet):
    """Return a material"""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class SignedProductDesignView(RetrieveAPIView):
    """Returned digitally signed product design"""
    queryset = ProductDesign.objects.all()
    serializer_class = ProductDesignSerializer

    def get_object(self, sku):
        return ProductDesign.objects.filter(sku=sku).first()

    def get(self, request, sku):
        serializer = self.get_serializer(self.get_object(sku))
        encoded = jwt.encode(serializer.data, 'SECRET', algorithm='HS256')
        return Response({'sku': sku, 'signed': encoded})
