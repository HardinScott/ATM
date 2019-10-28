from django.contrib import admin

from .models import AccountExtension, AtmCard, AtMachine, ATMachineRefill, Transaction

# Register your models here.

admin.site.register(AccountExtension)
admin.site.register(AtmCard)
admin.site.register(AtMachine)
#admin.site.register(ATMachineRefill)
#admin.site.register(Transaction)
