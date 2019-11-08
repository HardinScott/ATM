from django import forms
from . import models

class CashTransForm(forms.ModelForm):
    class Meta:
        model = models.Cash_Transfer
        fields = ['Beneficiary_Account_Number', 'Beneficiary_Name', 'Amout_Transferred']