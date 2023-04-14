from django import forms
from Importation.models import Importation

class ImportationForm(forms.ModelForm):
    class Meta:
        model=Importation
        fields='__all__'