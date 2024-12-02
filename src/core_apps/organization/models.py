from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Organization(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Organization Name"))
    logo = models.ImageField(upload_to='organization_logos/', verbose_name=_("Logo"), blank=True, null=True)
    address = models.TextField(verbose_name=_("Address"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), blank=True, null=True)
    website = models.URLField(verbose_name=_("Website"), blank=True, null=True)

    def __str__(self):
        return self.name

class OrganizationMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} - {self.role}"
