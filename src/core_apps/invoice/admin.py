from django.contrib import admin
from .models import Invoice
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('irn', 'title', 'client_name', 'organization_name', 'created_by', 'updated_by', 'issue_date', 'due_date', 'discount')  
    search_fields = ('irn', 'title', 'client__name', 'organization__name', 'created_by__email', 'updated_by__email')  
    list_filter = ('issue_date', 'due_date', 'organization', 'client', 'created_by', 'updated_by')
    readonly_fields = ('id', 'irn', 'created_by', 'updated_by', 'created_at', 'updated_at')  
    list_per_page = 25

    fieldsets = (
        ('Invoice Details', {
            'fields': (
                'id', 'irn', 'logo_url', 'title', 'organization', 'client', 'issue_date', 'due_date', 'items', 
                'payment_info', 'discount', 'terms_and_conditions', 'note'
            )
        }),
        ('Audit Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at')
        }),
    )

    def client_name(self, obj):
        return obj.client.name
    client_name.short_description = "Client"

    def organization_name(self, obj):
        return obj.organization.name
    organization_name.short_description = "Organization"

    def save_model(self, request, obj, form, change):
        """
        Override save_model to automatically set `created_by` and `updated_by` fields
        and validate date consistency.
        """
        if obj.due_date < obj.issue_date:
            raise ValueError("Due date cannot be earlier than issue date.")
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)
