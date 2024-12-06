from django.urls import path
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
    path("<int:id>/", OrganizationRetrieveUpdateDestroyView.as_view(), name="organization-retrieve-update-destroy"),
    path("members/", OrganizationMemberCreateView.as_view(), name="organization-member-create"),
    path("<int:pk>/upload-logo/", OrganizationLogoUploadView.as_view(), name="organization-upload-logo"),
    path("test/", OrganizationTestView.as_view(), name="organization-test"),
    path("user-organizations/", UserOrganizationsView.as_view(), name="user-organizations"),
]
