from rest_framework import serializers
from .models import Invoice
from core_apps.client.models import Organization, Client


class InvoiceListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source="client.name")
    organization = serializers.CharField(source="organization.name")

    class Meta:
        model = Invoice
        fields = ["id", "irn", "client", "organization", "issue_date", "due_date"]


class InvoiceListbyOrgSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source="client.name")

    class Meta:
        model = Invoice
        fields = ["id", "irn", "client", "issue_date", "due_date"]


class SimpleClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "email", "address", "phone_number"]


class SimpleOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "email", "address", "phone_number"]


class InvoiceDetailSerializer(serializers.ModelSerializer):
    client = SimpleClientSerializer()
    organization = SimpleOrganizationSerializer()
    created_by_info = serializers.CharField(source="created_by.email", read_only=True)
    updated_by_info = serializers.CharField(source="updated_by.email", read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        model = Invoice
        fields = [
            "id",
            "created_by_info",
            "updated_by_info",
            "logo_url",
            "title",
            "irn",
            "issue_date",
            "due_date",
            "client",
            "items",
            "payment_info",
            "discount",
            "shipping",
            "terms_and_conditions",
            "note",
            "template_id",
            "created_at",
            "updated_at",
            "organization",
        ]
        read_only_fields = ["irn"]


class InvoiceCreateSerializer(serializers.ModelSerializer):
    client = serializers.UUIDField()
    organization = serializers.UUIDField()

    class Meta:
        model = Invoice
        fields = [
            "logo_url",
            "title",
            "issue_date",
            "due_date",
            "client",
            "items",
            "payment_info",
            "discount",
            "shipping",
            "terms_and_conditions",
            "note",
            "template_id",
            "organization",
        ]

    def create(self, validated_data):
        """
        Custom create method to handle UUIDs for organization and client.
        """
        client_uuid = validated_data.pop("client")
        organization_uuid = validated_data.pop("organization")

        client = Client.objects.get(id=client_uuid)
        organization = Organization.objects.get(id=organization_uuid)

        invoice = Invoice.objects.create(
            **validated_data,
            client=client,
            organization=organization,
        )
        return invoice

    def update(self, instance, validated_data):
        """
        Custom update method to handle UUIDs for organization and client.
        """
        organization_uuid = validated_data.get("organization")
        client_uuid = validated_data.get("client")

        if organization_uuid:
            organization = Organization.objects.get(id=organization_uuid)
            instance.organization = organization

        if client_uuid:
            client = Client.objects.get(id=client_uuid)
            instance.client = client

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
