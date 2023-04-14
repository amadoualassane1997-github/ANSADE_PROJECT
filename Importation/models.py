from django.db import models

# Create your models here.
class Importation(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    total=models.FloatField()
    produits_alimentaires=models.FloatField()
    cosmetiques_chimiques=models.FloatField()
    produits_petroliers=models.FloatField()
    materiaux_de_construction=models.FloatField()
    voitures_et_pieces_detachees=models.FloatField()
    equipements=models.FloatField()
    autres_biens_de_consommation=models.FloatField()
    autres=models.FloatField()
class Meta:
    db_table='importation'