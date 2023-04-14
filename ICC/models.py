from django.db import models

# Create your models here.
class Icc(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    icc_global=models.FloatField()
    materiaux_de_construction=models.FloatField()
    biens_et_service_de_gestion_du_chantier=models.FloatField()
    location_de_materiels=models.FloatField()
    main_oeuvre=models.FloatField()
    materiaux_de_base=models.FloatField()
    materiaux_pour_couverture=models.FloatField()
    materiaux_de_menuiserie=models.FloatField()
    materiaux_de_plomberie_et_sanitaire=models.FloatField()
    materiaux_pour_travaux_electricite=models.FloatField()
    revetement_des_murs_et_sols=models.FloatField()
    peinture_vernis_chaux=models.FloatField()
    materiaux_pour_etancheite=models.FloatField()
class Meta:
    db_table='icc'