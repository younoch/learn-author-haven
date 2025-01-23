import logging
from uuid import UUID
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invoice, Organization
from .pagination import InvoicePagination
from .permissions import IsOwnerOrReadOnly
from .serializers import InvoiceListbyOrgSerializer, InvoiceDetailSerializer, InvoiceCreateSerializer

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

            if invoices_today.exists():
                last_invoice = invoices_today.first()
                last_increment = int(last_invoice.irn.split('-')[-1])
                return str(last_increment + 1).zfill(6)
            return "000001"

        except Exception as e:
            logger.error(f"Error retrieving increment number: {str(e)}", exc_info=True)
            raise
class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = InvoicePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ["created_at", "updated_at"]
    filterset_fields = ['organization']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InvoiceCreateSerializer
        return InvoiceListbyOrgSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        organization_id = self.request.query_params.get('organization_id')
        if organization_id:
            queryset = queryset.filter(organization__id=organization_id)
        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user, updated_by=self.request.user)
            logger.info(
                f"Invoice {serializer.data.get('irn')} created by {self.request.user.first_name}"
            )
        except Exception as e:
            logger.error(f"Error creating invoice: {str(e)}", exc_info=True)
            raise serializers.ValidationError({
                "error": "An unexpected error occurred while creating the invoice."
            })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "status": "success",
                "message": "Invoice created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            errors = e.detail
            error_messages = {field: error[0] if isinstance(error, list) else error for field, error in errors.items()}
            return Response({
                "status": "error",
                "message": "There are issues with the provided data. Please review the errors.",
                "errors": error_messages
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in creating invoice: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"

    def perform_update(self, serializer):
        try:
            instance = serializer.save(updated_by=self.request.user)
            instance.save()
        except Exception as e:
            logger.error(f"Error updating invoice: {str(e)}", exc_info=True)
            raise serializers.ValidationError({
                "error": "An unexpected error occurred while updating the invoice."
            })

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": "success",
                "message": "Invoice retrieved successfully",
                "data": serializer.data
            })
        except Http404:
            return Response({
                "status": "error",
                "message": "Invoice not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "message": "Invoice deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)
class InvoiceBulkDeleteView(generics.GenericAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({
                "status": "error",
                "message": "No IDs provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            uuids = [UUID(id) for id in ids]
            invoices = Invoice.objects.filter(id__in=uuids)
            invoices_deleted = invoices.count()
            invoices.delete()
            return Response({
                "status": "success",
                "message": f"{invoices_deleted} invoices deleted successfully.",
                "data": {}
            }, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}", exc_info=True)
            raise serializers.ValidationError({
                "error": f"Validation error: {str(ve)}"
            })
        except Invoice.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Some invoices do not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting invoices: {str(e)}", exc_info=True)
            raise serializers.ValidationError({
                "error": f"An unexpected error occurred: {str(e)}"
            })

class InvoiceTestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Test endpoint working!"}, status=status.HTTP_200_OK)
