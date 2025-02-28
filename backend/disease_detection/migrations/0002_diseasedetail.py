# Generated by Django 5.1.6 on 2025-02-23 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("disease_detection", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiseaseDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("disease_name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("causes", models.TextField()),
                ("symptoms", models.TextField()),
                ("prevention", models.TextField()),
                ("treatment", models.TextField()),
            ],
        ),
    ]
