from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('ref_no', 'title', 'created_by', 'updated_by', 'date', 'tax')
    search_fields = ('ref_no', 'title', 'created_by__email', 'updated_by__email')
    list_filter = ('date', 'created_by', 'updated_by')
    readonly_fields = ('id', 'tax')

    fieldsets = (
        (None, {
            'fields': (
                'id', 'created_by', 'updated_by', 'title', 'ref_no', 'date', 'client', 'items', 
                'payment_info', 'tax', 'terms_and_conditions', 'note'
            )
        }),
    )

admin.site.register(Invoice, InvoiceAdmin)
