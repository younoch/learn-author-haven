import logging

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice
from .pagination import InvoicePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import InvoiceJSONRenderer, InvoicesJSONRenderer
from .serializers import InvoiceSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = InvoicePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ["created_at", "updated_at"]
    renderer_classes = [InvoicesJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        logger.info(
            f"Invoice {serializer.data.get('ref_no')} created by {self.request.user.first_name}"
        )


class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [InvoiceJSONRenderer]
    parser_classes = [JSONParser]  # Use JSONParser for handling JSON data

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InvoiceTestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Test endpoint working!"}, status=200)
