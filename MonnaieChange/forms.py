from django import forms
from MonnaieChange.models import MonnaieChange


class MonnaieChangeForm(forms.ModelForm):
    class Meta:
        model=MonnaieChange
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}