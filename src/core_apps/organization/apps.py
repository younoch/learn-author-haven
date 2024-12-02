# from django.apps import AppConfig


# class OrganizationConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "organization"
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.organization"
    verbose_name = _("Organization")