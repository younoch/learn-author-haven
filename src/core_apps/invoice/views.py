import logging
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice, Organization
from .pagination import InvoicePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import InvoiceJSONRenderer, InvoicesJSONRenderer
from .serializers import InvoiceSerializer

User = get_user_model()

logger = logging.getLogger(__name__)

class GenerateIRNView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            organization_id = request.query_params.get('organization_id')
            if not organization_id:
                return JsonResponse(
                    {"error": "organization_id is required in query parameters."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            organization = get_object_or_404(Organization, id=organization_id)

            irn = self.generate_irn(organization)
            return Response({"irn": irn}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error generating IRN: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "An unexpected error occurred while generating the IRN."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def generate_irn(self, organization):
        from datetime import datetime
        try:
            today = datetime.today()
            date_str = today.strftime("%Y%m%d") 
            increment_number = self.get_increment_number(organization, date_str)
            return f"INV-{organization.invoice_reference_prefix}-{date_str}-{increment_number}"
        except Exception as e:
            logger.error(f"Error in IRN generation logic: {str(e)}", exc_info=True)
            raise

    def get_increment_number(self, organization, date_str):
        try:
            invoices_today = Invoice.objects.filter(
                organization=organization,
                irn__contains=date_str
            ).order_by('-irn')

            if invoices_today:
                last_invoice = invoices_today.first()
                last_increment = int(last_invoice.irn.split('-')[-1])
                return str(last_increment + 1).zfill(6)  
            return "000001" 

        except Exception as e:
            logger.error(f"Error retrieving increment number: {str(e)}", exc_info=True)
            raise

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
            f"Invoice {serializer.data.get('irn')} created by {self.request.user.first_name}"
        )
class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [InvoiceJSONRenderer]
    parser_classes = [JSONParser]  

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
