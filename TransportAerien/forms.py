from django import forms
from TransportAerien.models import TransportAerien


class TransportAerienForm(forms.ModelForm):
    class Meta:
        model=TransportAerien
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}