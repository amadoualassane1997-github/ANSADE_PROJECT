from django.db import models

# Create your models here.

class TraficTotalMaritime(models.Model):
    date=models.DateField(primary_key=True)
    trafic_total_tonnes=models.FloatField()
    total_nombre=models.IntegerField()
    port_ndb_trafic_total=models.FloatField()
    port_ndb_arrive_navires_nombre=models.IntegerField()
    trafic_total=models.FloatField()
    nombre_total_navires=models.IntegerField()
class Meta:
    db_table='trafic_total_maritime'