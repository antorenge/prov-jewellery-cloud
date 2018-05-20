"""
Validations API views
"""
import jwt
from rest_framework import viewsets, generics
from rest_framework.response import Response
from ..models import Validation, WorkInProgress
from .validation_serializer import ValidationSerializer
from .wip_serializer import WorkInProgressSerializer


class ValidationView(viewsets.ModelViewSet):
    """Return validations"""
    queryset = Validation.objects.all()
    serializer_class = ValidationSerializer


class WorkInProgressView(viewsets.ModelViewSet):
    """Return wip's"""
    queryset = WorkInProgress.objects.all()
    serializer_class = WorkInProgressSerializer


class SignedValidationView(generics.RetrieveAPIView):
    """Return digitally signed purchase order delivery"""
    queryset = Validation.objects.all()
    serializer_class = ValidationSerializer

    def get_object(self, id):
        return Validation.objects.filter(pk=id).first()

    def get(self, request, id):
        serializer = self.get_serializer(self.get_object(id))
        encoded = jwt.encode(serializer.data, 'SECRET', algorithm='HS256')
        return Response({'id': id, 'signed': encoded})
