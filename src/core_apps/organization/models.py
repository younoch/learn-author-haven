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

    # New Fields with Default Values and Nullability
    invoice_reference_prefix = models.CharField(
        max_length=10, 
        verbose_name=_("Invoice Reference Prefix"), 
        blank=True, 
        null=True, 
        default=""
    )
    default_template_id = models.IntegerField(
        verbose_name=_("Default Template ID"), 
        blank=True, 
        null=True, 
        default=1
    )
    theme_color = models.CharField(
        max_length=20, 
        verbose_name=_("Theme Color"), 
        blank=True, 
        null=True, 
        default="blue"
    )
    base_currency = models.CharField(
        max_length=10, 
        verbose_name=_("Base Currency"), 
        blank=True, 
        null=True, 
        default="USD"
    )
    time_zone = models.CharField(
        max_length=50, 
        verbose_name=_("Time Zone"), 
        blank=True, 
        null=True, 
        default="UTC"
    )
    business_type = models.CharField(
        max_length=50, 
        verbose_name=_("Business Type"), 
        blank=True, 
        null=True, 
        choices=[
            ("freelancing", "Freelancing"),
            ("ngo", "NGO"),
            ("profit_business", "Profit Business"),
        ],
        default="profit_business"
    )
    date_format = models.CharField(
        max_length=20, 
        verbose_name=_("Date Format"), 
        blank=True, 
        null=True, 
        default="YYYY-MM-DD"
    )
    terms_and_conditions = models.TextField(
        verbose_name=_("Terms and Conditions"), 
        blank=True, 
        null=True, 
        default="Default terms and conditions."
    )
    note = models.TextField(
        verbose_name=_("Note"), 
        blank=True, 
        null=True, 
        default="Additional notes."
    )
    invoice_expiry_days = models.IntegerField(
        verbose_name=_("Invoice Expiry Days"), 
        blank=True, 
        null=True, 
        default=30
    )

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
