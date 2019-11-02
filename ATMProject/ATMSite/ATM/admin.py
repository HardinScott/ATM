from django.contrib import admin

from .models import AccountExtension, AtmCard, AtMachine, ATMachineRefill, Transaction, Phone_Change, Pin_Change, Cash_Withdrawal, Cash_Transfer, Balance_Enquiry

# Register your models here.

admin.site.register(AccountExtension)
admin.site.register(AtmCard)
admin.site.register(AtMachine)
admin.site.register(ATMachineRefill)
admin.site.register(Transaction)
admin.site.register(Phone_Change)
admin.site.register(Pin_Change)
admin.site.register(Cash_Withdrawal)
admin.site.register(Cash_Transfer)
admin.site.register(Balance_Enquiry)
