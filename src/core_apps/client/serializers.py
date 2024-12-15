from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "organization_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone_number",
            "address",
            "organization_id",
        ]

class UpdateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone_number",
            "address",
        ]

class ClientListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization_id.name", read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "organization_name",
            "created_at",
            "updated_at",
        ]
