from django.db import models

# Create your models here.

class ConsomationCarbone(models.Model):
    date=models.DateField(primary_key=True)
    essence=models.FloatField()
    kerosene=models.FloatField()
    gas_oil=models.FloatField()
    fuel_oil=models.FloatField()
class Meta:
    db_table='consommation_carbone'