# Generated by Django 4.1.7 on 2023-04-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CroissanceMondiale",
            fields=[
                (
                    "trimestre",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("usa", models.FloatField()),
                ("france", models.FloatField()),
                ("allemagne", models.FloatField()),
                ("japon", models.FloatField()),
                ("royaume_uni", models.FloatField()),
                ("italie", models.FloatField()),
                ("canada", models.FloatField()),
            ],
        ),
    ]
