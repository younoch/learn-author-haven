import logging
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .models import Organization, OrganizationMember
from .serializers import OrganizationSerializer, OrganizationMemberSerializer, OrganizationListSerializer

User = get_user_model()

logger = logging.getLogger(__name__)

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"Organization {serializer.data.get('name')} created by {self.request.user.first_name}")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Organizations retrieved successfully",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Organization created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Organization retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": "success",
            "message": "Organization updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "message": "Organization deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)

class OrganizationMemberCreateView(generics.CreateAPIView):
    queryset = OrganizationMember.objects.all()
    serializer_class = OrganizationMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        organization = self.request.data.get("organization")
        user_id = self.request.data.get("user_id")

        # Check if the user is already a member of the organization
        if OrganizationMember.objects.filter(organization=organization, user_id=user_id).exists():
            raise serializers.ValidationError("User is already a member of this organization.")

        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Organization member added successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class OrganizationLogoUploadView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        id = self.kwargs["id"]
        organization = get_object_or_404(Organization, id=id)
        return organization

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'logo': request.data.get('logo')}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Organization logo updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class OrganizationTestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "status": "success",
            "message": "Organization test endpoint working!",
            "data": {}
        }, status=status.HTTP_200_OK)

class UserOrganizationsView(generics.GenericAPIView):
    serializer_class = OrganizationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        organizations = Organization.objects.filter(organizationmember__user=user)
        serializer = self.get_serializer(organizations, many=True)
        return Response({
            "status": "success",
            "message": "Organizations retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
