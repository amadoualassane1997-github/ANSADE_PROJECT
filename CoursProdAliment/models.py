from django.db import models

# Create your models here.

class CoursProdAliment(models.Model):
    date=models.DateField(primary_key=True)
    ble_eu_par_tonne=models.FloatField()
    riz_eu_par_tonne=models.FloatField()
    sucre_eu_par_tonne=models.FloatField()
    the_eu_par_tonne=models.FloatField()
    ble_mu_par_tonne=models.FloatField()
    riz_mu_par_tonne=models.FloatField()
    sucre_mu_par_tonne=models.FloatField()
    the_mu_par_tonne=models.FloatField()
class Meta:
    db_table='cours_prod_aliment'
