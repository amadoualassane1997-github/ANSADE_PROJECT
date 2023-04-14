from django.db import models

# Create your models here.

class SaisieElectricite(models.Model):
    date=models.DateField(primary_key=True)
    millions_de_kw_h=models.FloatField()
    mm_bt=models.FloatField()
    mm_mt=models.FloatField()
class Meta:
    db_table='saisie_electricite'