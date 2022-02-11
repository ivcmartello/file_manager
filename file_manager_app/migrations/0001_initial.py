# Generated by Django 4.0.2 on 2022-02-10 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Structure",
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
                ("name", models.CharField(max_length=50)),
                ("parent_id", models.IntegerField(default=0)),
                ("file_path", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
