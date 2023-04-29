from django.db import models

# Create your models here.

class CoursMatPrem(models.Model):
    date=models.DateField(primary_key=True)
    cours_mondiale_du_petrole=models.FloatField()
    prix_du_petrole_mauritanien=models.FloatField()
    cours_mondiale_du_minerai_fer_du_premier_seri=models.FloatField()
    prix_du_minerai_mauritanien=models.FloatField()
    cours_mondial_du_cuivre=models.FloatField()
    prix_du_cuivre_mauritanien=models.FloatField()
    cours_mondiale_or=models.FloatField()
    prix_or_mauritanien=models.FloatField()
    cours_mondiale_de_poisson=models.FloatField()
    prix_du_poisson_mauritanien=models.FloatField()
class Meta:
    db_table='cours_mat_prem'