from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class EauElectricite(models.Model):
    date=models.DateField(primary_key=True)
    eau_brute=models.FloatField()
    eau_nette=models.FloatField()
    elect_brute=models.FloatField()
    elect_nette=models.FloatField()
class Meta:
    db_table='eau_electricite'