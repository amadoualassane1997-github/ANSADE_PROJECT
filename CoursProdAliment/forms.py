from django import forms
from CoursProdAliment.models import CoursProdAliment

class CoursProdAlimentForm(forms.ModelForm):
    class Meta:
        model=CoursProdAliment
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}