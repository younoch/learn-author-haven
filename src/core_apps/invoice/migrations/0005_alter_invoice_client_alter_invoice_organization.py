# Generated by Django 4.1.7 on 2025-01-10 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0004_alter_organization_invoice_reference_prefix"),
        ("client", "0002_initial"),
        ("invoice", "0004_remove_invoice_ref_no_invoice_irn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Client",
                to="client.client",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Organization",
                to="organization.organization",
            ),
        ),
    ]
