from rest_framework import serializers
from .models import Invoice
from core_apps.client.models import Organization, Client

class InvoiceListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.name')
    organization = serializers.CharField(source='organization.name')

    class Meta:
        model = Invoice
        fields = ['id', 'irn', 'client', 'organization', 'issue_date', 'due_date']
class InvoiceListbyOrgSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.name')

    class Meta:
        model = Invoice
        fields = ['id', 'irn', 'client', 'issue_date', 'due_date']

class InvoiceDetailSerializer(serializers.ModelSerializer):
    client = serializers.UUIDField(format='hex_verbose')
    organization = serializers.UUIDField(format='hex_verbose')
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
            "terms_and_conditions",
            "note",
            "created_at",
            "updated_at",
            "organization",
        ]
        read_only_fields = ["irn"]

    def create(self, validated_data):
        organization_uuid = validated_data.pop("organization")
        client_uuid = validated_data.pop("client")

        organization = Organization.objects.get(id=organization_uuid)
        client = Client.objects.get(id=client_uuid)

        invoice = Invoice.objects.create(
            **validated_data,
            organization=organization,
            client=client,
        )
        return invoice

    def update(self, instance, validated_data):
        organization_uuid = validated_data.get("organization")
        client_uuid = validated_data.get("client")

        if organization_uuid:
            organization = Organization.objects.get(id=organization_uuid)
            instance.organization = organization

        if client_uuid:
            client = Client.objects.get(id=client_uuid)
            instance.client = client

        instance.logo_url = validated_data.get("logo_url", instance.logo_url)
        instance.title = validated_data.get("title", instance.title)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.items = validated_data.get("items", instance.items)
        instance.payment_info = validated_data.get("payment_info", instance.payment_info)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.terms_and_conditions = validated_data.get(
            "terms_and_conditions", instance.terms_and_conditions
        )
        instance.note = validated_data.get("note", instance.note)
        instance.save()
        return instance