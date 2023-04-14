from django.db import models

# Create your models here.
class TransportAerien(models.Model):
    date=models.DateField(primary_key=True)
    passagers_arrives=models.IntegerField()
    passagers_depart=models.IntegerField()
    total_passagers=models.IntegerField()
    mvmt_avion_arriv=models.IntegerField()
class Meta:
    db_table='trasport_aerien'