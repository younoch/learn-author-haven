from rest_framework.pagination import PageNumberPagination

class InvoicePagination(PageNumberPagination):
    page_size = 10
