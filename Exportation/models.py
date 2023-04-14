from django.db import models

# Create your models here.

class Exportation(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    total=models.FloatField()
    minerai_de_fer=models.FloatField()
    poisson=models.FloatField()
    petrole_brut=models.FloatField()
    Or=models.FloatField()
    cuivre=models.FloatField()
    autres=models.FloatField()
class Meta:
    db_table='exportation'