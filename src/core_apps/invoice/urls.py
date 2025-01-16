from django.urls import path
from .views import (
    InvoiceListCreateView, 
    InvoiceRetrieveUpdateDestroyView, 
    InvoiceBulkDeleteView,
    GenerateIRNView,
    InvoiceTestView, 
)

urlpatterns = [
    path("", InvoiceListCreateView.as_view(), name="invoice-list-create"),
    path("<uuid:id>/", InvoiceRetrieveUpdateDestroyView.as_view(), name="invoice-retrieve-update-destroy"),
    path("bulk-delete/", InvoiceBulkDeleteView.as_view(), name="invoice-bulk-delete"), 
    path("generate-irn/", GenerateIRNView.as_view(), name="generate-irn"), 
    path("test/", InvoiceTestView.as_view(), name="invoice-test"),
]
