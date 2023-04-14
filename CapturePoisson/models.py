from django.db import models

# Create your models here.
class CapturePoisson(models.Model):
    date=models.DateField(primary_key=True)
    pelagiques=models.FloatField()
    demersaux=models.FloatField()
    cephalopodes=models.FloatField()
    crustaces=models.FloatField()
    capture_total=models.FloatField()
class Meta:
    db_table='capture_poisson'