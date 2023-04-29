from django import forms
from IPI.models import Ipi

class IpiForm(forms.ModelForm):
    class Meta:
        model=Ipi
        fields='__all__'