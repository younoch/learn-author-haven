import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
from core_apps.organization.models import Organization

class Client(TimeStampedModel):
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="clients", 
        verbose_name=_("Organization"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Client Name"))
    address = models.TextField(verbose_name=_("Address"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "organization"],
                name="unique_email_per_organization"
            ),
            models.UniqueConstraint(
                fields=["phone_number", "organization"],
                name="unique_phone_number_per_organization"
            ),
        ]
