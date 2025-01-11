from django.urls import path
from .views import (
    InvoiceListCreateView, 
    InvoiceRetrieveUpdateDestroyView, 
    InvoiceTestView, 
    GenerateIRNView
)

urlpatterns = [
    path("", InvoiceListCreateView.as_view(), name="invoice-list-create"),
    path("<uuid:id>/", InvoiceRetrieveUpdateDestroyView.as_view(), name="invoice-retrieve-update-destroy"),
    path("test/", InvoiceTestView.as_view(), name="invoice-test"),
    path("generate-irn/", GenerateIRNView.as_view(), name="generate-irn"), 
]
