"""
Inventory API views
"""
from rest_framework import viewsets
from ..models import InventoryItem
from .serializers import InventoryItemSerializer


class InventoryItemView(viewsets.ModelViewSet):
    """Return inventory items"""
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
