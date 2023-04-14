from django.db import models

# Create your models here.
class CommerceExterieur(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    exportations=models.FloatField()
    importation=models.FloatField()
    solde_commercial=models.FloatField()
    tx_couv=models.FloatField()
class Meta:
    db_table='commerce_exterieur'