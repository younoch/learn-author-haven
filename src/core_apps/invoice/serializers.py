from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    created_by_info = serializers.CharField(source="created_by.email", read_only=True)
    updated_by_info = serializers.CharField(source="updated_by.email", read_only=True)
    client_details = serializers.JSONField(source='client')
    items_details = serializers.JSONField(source='items')
    payment_info_details = serializers.JSONField(source='payment_info')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        model = Invoice
        fields = [
            "id",
            "created_by_info",
            "updated_by_info",
            "title",
            "ref_no",
            "date",
            "client_details",
            "items_details",
            "payment_info_details",
            "tax",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        client_details = validated_data.pop("client")
        items_details = validated_data.pop("items")
        payment_info_details = validated_data.pop("payment_info")
        invoice = Invoice.objects.create(
            **validated_data,
            client=client_details,
            items=items_details,
            payment_info=payment_info_details
        )
        return invoice

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.ref_no = validated_data.get("ref_no", instance.ref_no)
        instance.date = validated_data.get("date", instance.date)
        instance.client = validated_data.get("client", instance.client)
        instance.items = validated_data.get("items", instance.items)
        instance.payment_info = validated_data.get("payment_info", instance.payment_info)
        instance.tax = validated_data.get("tax", instance.tax)
        instance.save()
        return instance
