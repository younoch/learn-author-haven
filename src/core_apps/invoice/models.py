from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core_apps.common.models import TimeStampedModel
from core_apps.client.models import Organization, Client
import uuid
from datetime import datetime

User = get_user_model()

class Invoice(TimeStampedModel):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_invoices")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_invoices")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invoices")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    irn = models.CharField(max_length=255, verbose_name=_("Invoice Reference Number"), unique=True, blank=True)
    date = models.DateField(verbose_name=_("Date"))

    # Invoice Items
    items = models.JSONField(verbose_name=_("Invoice Items"))

    # Payment Info
    payment_info = models.JSONField(verbose_name=_("Payment Info"))

    # Totals
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Tax"))

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

    def __str__(self):
        return f"Invoice {self.irn} for {self.client.name}"

    def save(self, *args, **kwargs):
        if not self.irn:
            # Generate IRN based on the format
            irn_prefix = self.organization.invoice_reference_prefix or "INV"
            current_date = datetime.now().strftime("%Y%m%d")
            increment_number = self.get_incremental_number(current_date)
            self.irn = f"{irn_prefix}-{current_date}-{increment_number}"
        super().save(*args, **kwargs)

    def get_incremental_number(self, date):
        """
        Fetch the last invoice for the current date to generate the next incremental number.
        """
        last_invoice = Invoice.objects.filter(irn__startswith=f"{self.organization.invoice_reference_prefix}-{date}").order_by('-irn').first()
        if last_invoice:
            last_number = last_invoice.irn.split('-')[-1]
            next_number = str(int(last_number) + 1).zfill(6)  # Increment and ensure it is 6 digits
        else:
            next_number = "000001"  # Start from 000001 for the first invoice of the day
        return next_number
