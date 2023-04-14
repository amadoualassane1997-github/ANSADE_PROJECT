from django.db import models

# Create your models here.
class ProductionCuivreOr(models.Model):
    trimestre=models.CharField(max_length=10,primary_key=True)
    production_cuivre=models.FloatField()
    or_quantite_en_oz_total=models.FloatField()
class Meta:
    db_table='production_cuivre_or'