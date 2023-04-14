from django import forms
from ConsomationCarbone.models import ConsomationCarbone

class ConsomationCarboneForm(forms.ModelForm):
    class Meta:
        model=ConsomationCarbone
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}