# Generated by Django 3.1.7 on 2021-04-04 09:16

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("mysite", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership_form",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "ACardNum",
                    models.CharField(
                        default="", max_length=20, null=True, verbose_name="aCardNum"
                    ),
                ),
                (
                    "num_months",
                    models.PositiveIntegerField(
                        default=1, null=True, verbose_name="num_months"
                    ),
                ),
                (
                    "cert",
                    models.FileField(
                        blank=True, null=True, upload_to="", verbose_name="cert"
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(
                        blank=True, default=True, null=True, verbose_name="is_approved"
                    ),
                ),
                (
                    "phone_num",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        null=True,
                        region=None,
                        verbose_name="phone_num",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=150,
                        null=True,
                        verbose_name="reason",
                    ),
                ),
                (
                    "removed",
                    models.BooleanField(
                        blank=True, default=False, null=True, verbose_name="removed"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mysite.newuser",
                    ),
                ),
            ],
        ),
    ]
