from django import forms
from ProductionCuivreOr.models import ProductionCuivreOr

class ProductionCuivreOrForm(forms.ModelForm):
    class Meta:
        model=ProductionCuivreOr
        fields='__all__'
