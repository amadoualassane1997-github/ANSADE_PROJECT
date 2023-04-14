from django import forms
from INPC.models import Inpc

class InpcForm(forms.ModelForm):
    class Meta:
        model=Inpc
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}