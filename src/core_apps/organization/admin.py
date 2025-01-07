from django.contrib import admin
from .models import Organization, OrganizationMember

class OrganizationMemberInline(admin.TabularInline):
    model = OrganizationMember
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone_number', 'website', 'created_at', 'updated_at',
        'invoice_reference_prefix', 'default_template_id', 'theme_color', 'base_currency', 
        'time_zone', 'business_type', 'date_format', 'invoice_expiry_days'
    )
    search_fields = ('name', 'email', 'phone_number', 'invoice_reference_prefix', 'base_currency')
    list_filter = ('created_at', 'updated_at', 'business_type', 'base_currency')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'id', 'name', 'logo', 'address', 'email', 'phone_number', 'website', 
                'invoice_reference_prefix', 'default_template_id', 'theme_color', 'base_currency', 
                'time_zone', 'business_type', 'date_format', 'terms_and_conditions', 'note', 
                'invoice_expiry_days', 'created_at', 'updated_at'
            )
        }),
    )
    inlines = [OrganizationMemberInline]

class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')
    search_fields = ('user__email', 'organization__name', 'role')
    list_filter = ('role',)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMember, OrganizationMemberAdmin)
