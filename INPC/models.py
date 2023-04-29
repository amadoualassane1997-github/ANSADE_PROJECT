from django.db import models

# Create your models here.

class Inpc(models.Model):
    date=models.DateField(primary_key=True)
    inpc_global=models.FloatField()
    produits_alimentaires_et_boissons_non_alcolises=models.FloatField()
    tabac_et_stupefiant=models.FloatField()
    articles_habillement_et_chaussures=models.FloatField()
    logement_eau_gaz_electricites_et_autre_combistible=models.FloatField()
    meubles_articles_de_menages_et_entretient_courant_du_foyer=models.FloatField()
    sante=models.FloatField()
    transport=models.FloatField()
    communication=models.FloatField()
    loisir_et_culture=models.FloatField()
    enseignement=models.FloatField()
    restaurant_et_hotel=models.FloatField()
    bien_et_service_diver=models.FloatField()
class Meta:
    db_table='inpc'