from django import forms
from InflationMondiale.models import InflationMondiale

class InflationMondialeForm(forms.ModelForm):
    class Meta:
        model=InflationMondiale
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}