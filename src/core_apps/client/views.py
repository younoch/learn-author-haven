from rest_framework import generics, status, permissions, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Client
from .serializers import (
    ClientSerializer,
    CreateClientSerializer,
    UpdateClientSerializer,
    ClientListSerializer,
)
from core_apps.organization.models import Organization
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "email", "phone_number"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        organization_uuid = self.request.data.get('organization')  
        try:
            organization = Organization.objects.get(id=organization_uuid)
        except Organization.DoesNotExist:
            raise serializers.ValidationError({
                "organization": ["Organization not found."]
            })

        existing_client = Client.objects.filter(
            email=self.request.data.get('email'), organization=organization
        ).first()
        if existing_client:
            raise serializers.ValidationError({
                "email": ["Client with this email already exists for the organization."]
            })

        serializer.save(organization=organization)

    def create(self, request, *args, **kwargs):
        serializer = CreateClientSerializer(data=request.data)
        try:
            # Validate the serializer
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # If everything is valid, return a success response
            return Response({
                "status": "success",
                "message": "Client created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            # Handle field-specific errors
            errors = e.detail
            error_messages = {}
            for field, error in errors.items():
                error_messages[field] = error[0] if isinstance(error, list) else error

            return Response({
                "status": "error",
                "message": "Validation failed",
                "errors": error_messages
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle unexpected exceptions
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Client retrieved successfully",
            "data": serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdateClientSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": "success",
            "message": "Client updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "message": "Client deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)


class OrganizationClientsView(generics.ListAPIView):
    serializer_class = ClientListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organization_uuid = self.kwargs.get("organization_uuid") 
        return Client.objects.filter(organization__id=organization_uuid)

    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()
        serializer = self.get_serializer(clients, many=True)
        return Response({
            "status": "success",
            "message": "Clients retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
