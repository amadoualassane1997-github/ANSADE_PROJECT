# Generated by Django 4.1.7 on 2023-04-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CoursMatPrem", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="coursmatprem", name="id",),
        migrations.AlterField(
            model_name="coursmatprem",
            name="date",
            field=models.DateField(primary_key=True, serialize=False),
        ),
    ]
