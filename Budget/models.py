from django.db import models

# Create your models here.


class Budget(models.Model):
    date=models.DateField(primary_key=True)
    rectettes_totales=models.FloatField()
    recettes_fiscales=models.FloatField()
    recettes_non_fiscales=models.FloatField()
    recettes_petro_net=models.FloatField()
    dont=models.FloatField()
    depences_et_prets_net=models.FloatField()
    depences_courant=models.FloatField()
    depences_equipe_et_prets_net=models.FloatField()
    restructurations_equipe_et_prets_net=models.FloatField()
    solde_globale_dons_compris=models.FloatField()
class Meta:
    db_table='budget'
