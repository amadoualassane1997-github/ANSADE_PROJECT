# Generated by Django 4.1.7 on 2023-04-13 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ICC", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="icc", old_name="date", new_name="trimestre",
        ),
    ]
