from rest_framework import serializers
from .models import Organization, OrganizationMember
from django.contrib.auth import get_user_model

User = get_user_model()

class OrganizationMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id')
    user_name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = OrganizationMember
        fields = ['user_id', 'user_name', 'role', 'organization']

class OrganizationSerializer(serializers.ModelSerializer):
    members = OrganizationMemberSerializer(source='organizationmember_set', many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "logo",
            "address",
            "email",
            "phone_number",
            "website",
            "invoice_reference_prefix",
            "default_template_id",
            "base_currency",
            "time_zone",
            "business_type",
            "date_format",
            "terms_and_conditions",
            "note",
            "invoice_expiry_days",
            "members",
            "theme_color",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        organization = Organization.objects.create(**validated_data)
        # Add the creator as the first member with the owner role
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            OrganizationMember.objects.create(user=request.user, organization=organization, role='owner')
        return organization

    def update(self, instance, validated_data):
        # Update all fields, including new ones
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

class OrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id", 
            "name", 
            "logo", 
            "address", 
            "email", 
            "phone_number", 
            "website",
            "invoice_reference_prefix",
            "default_template_id",
            "base_currency",
            "terms_and_conditions",
            "note",
            "invoice_expiry_days",
            "theme_color",
        ]
