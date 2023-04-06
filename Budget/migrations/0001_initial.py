# Generated by Django 4.1.7 on 2023-04-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Budget",
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
                ("rectettes_totales", models.FloatField()),
                ("recettes_fiscales", models.FloatField()),
                ("recettes_non_fiscales", models.FloatField()),
                ("recettes_petro_net", models.FloatField()),
                ("dont", models.FloatField()),
                ("depences_et_prets_net", models.FloatField()),
                ("depences_courant", models.FloatField()),
                ("depences_equipe_et_prets_net", models.FloatField()),
                ("restructurations_equipe_et_prets_net", models.FloatField()),
                ("solde_globale_dons_compris", models.FloatField()),
            ],
        ),
    ]
