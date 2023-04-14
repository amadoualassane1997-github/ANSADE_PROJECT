from django.db import models

# Create your models here.

class Inpc(models.Model):
    date=models.DateField(primary_key=True)
    inpc_global=models.FloatField()
    prod_alim_et_boiss_non_alcool_fr=models.FloatField()
    tabac_et_stupefiant=models.FloatField()
    art_habmnt_et_chauss=models.FloatField()
    log_eau_gaz_elec_et_autre_combtible=models.FloatField()
    meub_art_menage_et_entre_courant_du_foyer=models.FloatField()
    sante=models.FloatField()
    transport=models.FloatField()
    communication=models.FloatField()
    loisir_et_culture=models.FloatField()
    enseignement=models.FloatField()
    restaurant_et_hotel=models.FloatField()
    bien_et_service_diver=models.FloatField()
class Meta:
    db_table='inpc'