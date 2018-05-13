"""
Products API views
"""
from rest_framework import viewsets, mixins, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProductDesign
from .serializers import ProductDesignSerializer


class ProductDesignView(viewsets.ModelViewSet):
    """Return a product design"""
    queryset = ProductDesign.objects.all()
    serializer_class = ProductDesignSerializer

    # filter the collections
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filter_fields = ('sku', 'name')

    search_fields = ('sku', 'name')
    ordering_fields = ('date_created',)
