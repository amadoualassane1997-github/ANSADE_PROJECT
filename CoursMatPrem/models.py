from django.db import models

# Create your models here.

class CoursMatPrem(models.Model):
    date=models.DateField(primary_key=True)
    cours_mon_pet=models.FloatField()
    prix_pet_mr=models.FloatField()
    cours_mon_min_fer_prem_seri=models.FloatField()
    prix_min_mr=models.FloatField()
    cours_mon_cuivre=models.FloatField()
    prix_cuivre_mr=models.FloatField()
    cours_mon_or=models.FloatField()
    prix_or_mr=models.FloatField()
    cours_mon_poisson=models.FloatField()
    prix_poisson_mr=models.FloatField()
class Meta:
    db_table='cours_mat_prem'