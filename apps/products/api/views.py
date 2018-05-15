"""
Products API views
"""
import jwt
from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProductDesign, Material
from .serializers import (ProductDesignSerializer, MaterialSerializer,
                          ValidateSerializer)


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


class SignedProductDesignView(generics.RetrieveAPIView):
    """Returned digitally signed product design"""
    queryset = ProductDesign.objects.all()
    serializer_class = ProductDesignSerializer

    def get_object(self, sku):
        return ProductDesign.objects.filter(sku=sku).first()

    def get(self, request, sku):
        serializer = self.get_serializer(self.get_object(sku))
        encoded = jwt.encode(serializer.data, 'SECRET', algorithm='HS256')
        return Response({'sku': sku, 'token': encoded})


class ValidateJWTView(generics.CreateAPIView):
    """Validate jwt tokens"""
    serializer_class = ValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = ValidateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = bytes(serializer.data['token'], 'utf-8')
                jwt.decode(token, 'SECRET', algorithms='HS256')
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except jwt.InvalidSignatureError as error:
                return Response({'error': str(error)},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
