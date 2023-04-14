from django import forms
from TraficTotalMaritime.models import TraficTotalMaritime


class TraficTotalMaritimeForm(forms.ModelForm):
    class Meta:
        model=TraficTotalMaritime
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}