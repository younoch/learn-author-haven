from django.urls import path, re_path
from .views import (
    OrganizationListCreateView,
    OrganizationRetrieveUpdateDestroyView,
    OrganizationMemberCreateView,
    OrganizationLogoUploadView,
    OrganizationTestView,
    UserOrganizationsView
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organization-list-create"),
    re_path(r"^(?P<id>[0-9a-f-]+)/$", OrganizationRetrieveUpdateDestroyView.as_view(), name="organization-retrieve-update-destroy"),
    path("members/", OrganizationMemberCreateView.as_view(), name="organization-member-create"),
    path("<uuid:id>/upload-logo/", OrganizationLogoUploadView.as_view(), name="organization-upload-logo"),  # Ensure the type matches
    path("test/", OrganizationTestView.as_view(), name="organization-test"),
    path("user-organizations/", UserOrganizationsView.as_view(), name="user-organizations"),
]
