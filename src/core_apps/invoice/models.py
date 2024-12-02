from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core_apps.common.models import TimeStampedModel
from core_apps.client.models import Organization, Client

User = get_user_model()

class Invoice(TimeStampedModel):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_invoices")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_invoices")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invoices")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    ref_no = models.CharField(max_length=50, verbose_name=_("Reference Number"))
    date = models.DateField(verbose_name=_("Date"))

    # Invoice Items
    items = models.JSONField(verbose_name=_("Invoice Items"))

    # Payment Info
    payment_info = models.JSONField(verbose_name=_("Payment Info"))

    # Totals
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Tax"))

    def __str__(self):
        return f"Invoice {self.ref_no} for {self.client.name}"
