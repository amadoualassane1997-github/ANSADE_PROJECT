from django import forms
from EauElectricite.models import EauElectricite

class EauElectriciteForm(forms.ModelForm):
    class Meta:
        model=EauElectricite
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}