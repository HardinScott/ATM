from django import forms
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class CashTransForm(forms.ModelForm):
    class Meta:
        model = models.Cash_Transfer
        fields = ['Beneficiary_Account_Number', 'Beneficiary_Name', 'Amout_Transferred']


class CashTransNotLoginForm(forms.ModelForm):
    card_number = forms.IntegerField()
    pin = forms.IntegerField()

    class Meta(CashTransForm.Meta):
        fields = ['card_number', 'pin'] + CashTransForm.Meta.fields


class CashWithdrawalForm(forms.ModelForm):
    class Meta:
        model = models.Cash_Withdrawal
        fields = ['Amount_Transferred']


class CashWithdrawalNotLoginForm(forms.ModelForm):
    card_number = forms.IntegerField()
    pin = forms.IntegerField()

    class Meta(CashWithdrawalForm.Meta):
        fields = ['card_number', 'pin'] + CashWithdrawalForm.Meta.fields


class CardAndPinForm(forms.Form):
    card_number = forms.IntegerField()
    pin = forms.IntegerField()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
