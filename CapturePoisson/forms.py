from django import forms
from CapturePoisson.models import CapturePoisson

class CapturePoissonForm(forms.ModelForm):
    class Meta:
        model=CapturePoisson
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type': 'date'})}