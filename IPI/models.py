from django.db import models

# Create your models here.

class Ipi(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    indice_general=models.FloatField()
    indice_industries_extractives=models.FloatField()
    indice_des_industries_manufacturieres=models.FloatField()
    indice_de_energie=models.FloatField()
    extraction_de_minerais_metaliques=models.FloatField()
    fabrication_de_produits_alimentaires=models.FloatField()
    fabrication_de_boisson=models.FloatField()
    travail_de_cuir=models.FloatField()
    travail_du_bois_et_fabrication_articles_en_bois_hors_meubles=models.FloatField()
    fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton=models.FloatField()
    fabrication_de_produits_chimiques=models.FloatField()
    travail_de_caoutchouc_et_du_plastique=models.FloatField()
    fabrication_de_materiaux_mineraux=models.FloatField()
    metalurgie=models.FloatField()
    fabrication_autres_materiel_de_transport=models.FloatField()
    autres_industries_manufacturieres=models.FloatField()
    production_et_distribution_electricite=models.FloatField()
    captage_traitement_et_distribution_eau=models.FloatField()
class Meta:
    db_table='ipi'