# Generated by Django 4.1.7 on 2023-04-25 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "INPC",
            "0002_rename_art_habmnt_et_chauss_inpc_artucles_habillement_et_chaussures_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="inpc",
            old_name="artucles_habillement_et_chaussures",
            new_name="articles_habillement_et_chaussures",
        ),
    ]
