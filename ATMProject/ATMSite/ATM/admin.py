from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from ATM.models import *
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.
User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'Account_Number')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'Account_Number',)}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class AccountExtensionAdmin(admin.ModelAdmin):
    list_display = ('Account_Number', 'Name')


class AtmCardAdmin(admin.ModelAdmin):
    list_display = ('Atm_Card_Number', 'Account_Number', 'Name')


class Cash_TransferAdmin(admin.ModelAdmin):
    list_display = ('Cash_Withdrawal_ID', 'Transaction_ID', 'Beneficiary_Account_Number')


admin.site.register(AccountExtension, AccountExtensionAdmin)
admin.site.register(AtmCard, AtmCardAdmin)
admin.site.register(AtMachine)
admin.site.register(ATMachineRefill)
admin.site.register(Transaction)
admin.site.register(Phone_Change)
admin.site.register(Pin_Change)
admin.site.register(Cash_Withdrawal)
admin.site.register(Cash_Transfer, Cash_TransferAdmin)
admin.site.register(Balance_Enquiry)
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
