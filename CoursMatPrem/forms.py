from django import forms
from CoursMatPrem.models import CoursMatPrem

class CoursMatPremForm(forms.ModelForm):
    class Meta:
        model=CoursMatPrem
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}