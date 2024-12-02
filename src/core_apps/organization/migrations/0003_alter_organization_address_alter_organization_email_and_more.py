# Generated by Django 4.1.7 on 2024-12-01 18:42

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0002_remove_organization_parent_organization_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="address",
            field=models.TextField(blank=True, null=True, verbose_name="Address"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="Email"
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                verbose_name="Phone Number",
            ),
        ),
    ]
