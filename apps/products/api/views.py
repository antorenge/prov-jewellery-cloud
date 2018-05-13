"""
Products API views
"""
from rest_framework import viewsets, mixins, status, filters
from ..models import ProductDesign
from .serializers import ProductDesignSerializer


class ProductDesignView(viewsets.ModelViewSet):
    """Return a product design"""
    queryset = ProductDesign.objects.all()
    serializer_class = ProductDesignSerializer

    # filter the collections
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,
    #                    filters.OrderingFilter)
    # filter_fields = ('collection', 'collection__code', 'collection__id', 'sku',
    #                  'name', 'product_state', 'category__name',
    #                  'group_category__name', 'year', 'quarter', 'color',)

    # search_fields = ('name', 'status', 'sku')
    # ordering_fields = ('date_created', 'status')
