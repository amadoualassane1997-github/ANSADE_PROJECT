# Generated by Django 4.1.7 on 2023-04-07 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConsomationCarbone",
            fields=[
                ("date", models.DateField(primary_key=True, serialize=False)),
                ("essence", models.FloatField()),
                ("kerosene", models.FloatField()),
                ("gas_oil", models.FloatField()),
                ("fuel_oil", models.FloatField()),
            ],
        ),
    ]