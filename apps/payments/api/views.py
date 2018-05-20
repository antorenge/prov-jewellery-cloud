"""
Payments API views
"""
import jwt
from rest_framework import viewsets, generics
from rest_framework.response import Response
from ..models import OwnershipTransfer
from .serializers import OwnershipTransferSerializer


class OwnershipTransferView(viewsets.ModelViewSet):
    """Return ownership transfers"""
    queryset = OwnershipTransfer.objects.all()
    serializer_class = OwnershipTransferSerializer


class SignedTransferView(generics.RetrieveAPIView):
    """Return digitally signed ownership transfer"""
    queryset = OwnershipTransfer.objects.all()
    serializer_class = OwnershipTransferSerializer

    def get_object(self, id):
        return OwnershipTransfer.objects.filter(pk=id).first()

    def get(self, request, id):
        serializer = self.get_serializer(self.get_object(id))
        encoded = jwt.encode(serializer.data, 'SECRET', algorithm='HS256')
        return Response({'id': id, 'signed': encoded})
