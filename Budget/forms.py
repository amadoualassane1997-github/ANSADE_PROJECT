from django import forms
from Budget.models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model=Budget
        fields='__all__'
        widgets={'date':forms.widgets.DateInput(attrs={'type':'date'})}