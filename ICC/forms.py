from django import forms
from ICC.models import Icc

class IccForm(forms.ModelForm):
    class Meta:
        model=Icc
        fields='__all__'