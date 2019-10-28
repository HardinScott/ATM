from django.db import models

# Create your models here.

class AccountExtension(models.Model):
	Account_Number = models.AutoField(primary_key=True)
	Name = models.CharField(max_length=60)
	Phone_Number = models.CharField(max_length=20)
	Balance = models.DecimalField(max_digits=20, decimal_places = 10,default=0)

class AtmCard(models.Model):
	Atm_Card_Number = models.AutoField(primary_key=True)
	Account_Number = models.ForeignKey(AccountExtension, on_delete=models.PROTECT,)
	PIN = models.IntegerField()
	Name = models.CharField(max_length=60)
	Date_Of_Issue = models.DateField(auto_now_add=True)
	Expiry_Date = models.DateField(auto_now_add=True)
	Address = models.CharField(max_length=100)
	Two_Factor_Authentication_Status = models.BooleanField()
	Phone_Number = models.CharField(max_length=20)
	Card_Status = models.CharField(max_length=50)

class AtMachine(models.Model):
	At_Machine_UID = models.AutoField(primary_key = True)
	Current_Balance = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	Location = models.CharField(max_length=100)
	MinimumBalance = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	Status = models.CharField(max_length=50)
	Last_Refill_Date = models.DateField()
	Next_Maintenance_Date = models.DateField()

class ATMachineRefill:
	Refill_ID = models.AutoField(primary_key = True)
	At_Machine_UID = models.ForeignKey(AtMachine, on_delete=models.PROTECT)
	Amount = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	ATM_Branch = models.CharField(max_length=100)
	Refill_Date = models.DateField()
	Previous_Balance = models.DecimalField(max_digits=25,decimal_places=0,default=0)

class Transaction:
	Transaction_ID = models.AutoField(primary_key=True)
	ATM_Card_Number = models.ForeignKey(AtmCard, on_delete=models.PROTECT)
	Date = models.DateField()
	At_Machine_UID = models.ForeignKey(AtMachine, on_delete=models.PROTECT)
	Status = models.CharField(max_length=50)
	Response_Code = models.CharField(max_length=256)
	Type_Of_Transaction = models.CharField(max_length=50)


