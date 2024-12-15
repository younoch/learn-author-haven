from django.urls import path, re_path
from .views import (
    ClientListCreateView,
    ClientRetrieveUpdateDestroyView,
    OrganizationClientsView,
)

urlpatterns = [
    # List and create clients
    path("", ClientListCreateView.as_view(), name="client-list-create"),
    re_path(r"^(?P<id>[0-9a-f-]+)/$", ClientRetrieveUpdateDestroyView.as_view(), name="client-retrieve-update-destroy"),
    path("clients-by-organization/<uuid:organization_id>/", OrganizationClientsView.as_view(), name="organization-clients"),
]
