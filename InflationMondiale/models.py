from django.db import models

# Create your models here.

class InflationMondiale(models.Model):
    date=models.DateField(primary_key=True)
    usa=models.FloatField()
    france=models.FloatField()
    allemagne=models.FloatField()
    japon=models.FloatField()
    royaume_uni=models.FloatField()
    italie=models.FloatField()
    canada=models.FloatField()
class Meta:
    db_table='inflation_mondiale'