from django import forms
from CroissanceMondiale.models import CroissanceMondiale

class CroissanceMondialeForm(forms.ModelForm):
    class Meta:
        model=CroissanceMondiale
        fields='__all__'