from django_filters import rest_framework as filters
from .models import Invoice

class InvoiceFilter(filters.FilterSet):
    class Meta:
        model = Invoice
        fields = {
            'ref_no': ['exact', 'icontains'],
            'created_by': ['exact'],
            'updated_by': ['exact'],
            'date': ['exact', 'lte', 'gte'],
        }
