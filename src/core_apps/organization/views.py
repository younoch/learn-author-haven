import logging
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization, OrganizationMember
from .serializers import OrganizationSerializer, OrganizationMemberSerializer

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

class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class OrganizationMemberCreateView(generics.CreateAPIView):
    queryset = OrganizationMember.objects.all()
    serializer_class = OrganizationMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        organization_id = self.request.data.get("organization")
        user_id = self.request.data.get("user_id")

        # Check if the user is already a member of the organization
        if OrganizationMember.objects.filter(organization_id=organization_id, user_id=user_id).exists():
            raise serializers.ValidationError("User is already a member of this organization.")

        serializer.save()

class OrganizationLogoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def patch(self, request, pk, format=None):
        organization = get_object_or_404(Organization, pk=pk)
        logo = request.data.get('logo')

        if logo:
            organization.logo = logo
            organization.save()
            return Response({"message": "Logo updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "No logo file provided"}, status=status.HTTP_400_BAD_REQUEST)

class OrganizationTestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Organization test endpoint working!"}, status=200)
