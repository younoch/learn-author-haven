import uuid
from rest_framework import serializers
from .models import Client
from core_apps.organization.models import Organization

class ClientSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(source='organization.id', read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

class CreateClientSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone_number",
            "address",
            "organization",
        ]

    def validate_organization(self, value):
        try:
            uuid_obj = uuid.UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format for organization field.")
        if not Organization.objects.filter(id=uuid_obj).exists():
            raise serializers.ValidationError("Organization with this ID does not exist.")
        return uuid_obj
class UpdateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone_number",
            "address",
            "organization",
        ]


class ClientListSerializer(serializers.ModelSerializer):
    # Include organization name for readability
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "organization_name",
            "organization",
            "created_at",
            "updated_at",
        ]
