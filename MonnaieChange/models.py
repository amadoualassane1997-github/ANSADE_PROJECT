from django.db import models


# Create your models here.


class MonnaieChange(models.Model):
    date=models.DateField(primary_key=True)
    dollar_des_u_e=models.FloatField()
    euro=models.FloatField()
    sterling=models.FloatField()
    yen=models.FloatField()
    dirham_marocain=models.FloatField()
    dinar_tunisien=models.FloatField()
    dinar_algerien=models.FloatField()
    franc_cfa=models.FloatField()
    dts=models.FloatField()
class Meta:
    db_table='monnaie_change'

