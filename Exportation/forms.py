from django import forms
from Exportation.models import Exportation

class ExportationForm(forms.ModelForm):
    class Meta:
        model=Exportation
        fields='__all__'