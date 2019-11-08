from django.contrib import admin

from ATM.models import *

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
