# Generated by Django 4.1.7 on 2023-03-29 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CoursMatPrem",
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
                ("date", models.DateField()),
                ("cours_mon_pet", models.FloatField()),
                ("prix_pet_mr", models.FloatField()),
                ("cours_mon_min_fer_prem_seri", models.FloatField()),
                ("prix_min_mr", models.FloatField()),
                ("cours_mon_cuivre", models.FloatField()),
                ("prix_cuivre_mr", models.FloatField()),
                ("cours_mon_or", models.FloatField()),
                ("prix_or_mr", models.FloatField()),
                ("cours_mon_poisson", models.FloatField()),
                ("prix_poisson_mr", models.FloatField()),
            ],
        ),
    ]
