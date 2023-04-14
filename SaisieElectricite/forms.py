from django import forms
from SaisieElectricite.models import SaisieElectricite


class SaisieElectriciteForm(forms.ModelForm):
    class Meta:
        model=SaisieElectricite
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}