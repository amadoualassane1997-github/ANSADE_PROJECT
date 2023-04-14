from django import forms
from CommerceExterieur.models import CommerceExterieur

class CommerceExterieurForm(forms.ModelForm):
    class Meta:
        model=CommerceExterieur
        fields='__all__'