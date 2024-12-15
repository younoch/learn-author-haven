from rest_framework import generics, status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer, CreateClientSerializer, UpdateClientSerializer, ClientListSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "email", "phone_number"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = CreateClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Client created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

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
        organization_id = self.kwargs.get("organization_id")
        return Client.objects.filter(organization_id=organization_id)

    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()
        serializer = self.get_serializer(clients, many=True)
        return Response({
            "status": "success",
            "message": "Clients retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
