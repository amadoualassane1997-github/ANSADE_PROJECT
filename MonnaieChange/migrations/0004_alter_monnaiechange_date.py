# Generated by Django 4.1.7 on 2023-03-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MonnaieChange", "0003_rename_dolllar_des_u_e_monnaiechange_dollar_des_u_e"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monnaiechange", name="date", field=models.DateField(),
        ),
    ]