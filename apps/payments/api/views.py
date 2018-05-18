"""
Payments API views
"""
from rest_framework import viewsets
from ..models import OwnershipTransfer
from .serializers import OwnershipTransferSerializer


class OwnershipTransferView(viewsets.ModelViewSet):
    """Return ownership transfers"""
    queryset = OwnershipTransfer.objects.all()
    serializer_class = OwnershipTransferSerializer
