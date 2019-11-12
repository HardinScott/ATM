from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from random import randint

# Create your models here.

class AccountExtension(models.Model):
	Account_Number = models.AutoField(primary_key=True)
	Name = models.CharField(max_length=60)
	Phone_Number = models.CharField(max_length=20)
	Balance = models.DecimalField(max_digits=20, decimal_places = 10,default=0)

	def save(self):
		if not self.Account_Number: #if this account is being saved for the first time now
			is_unique = False
			while not is_unique:
				AccNum = randint(10000000, 99999999)
				is_unique = (AccountExtension.objects.filter(Account_Number=AccNum).count() == 0)
			self.Account_Number = AccNum
		super(AccountExtension, self).save()

	def __str__(self):
		return str(self.Account_Number)

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

	def save(self):
		if not self.Atm_Card_Number: #if this account is being saved for the first time now
			is_unique = False
			while not is_unique:
				CardNum = randint(1000000000000000, 9999999999999999)
				is_unique = (AtmCard.objects.filter(Atm_Card_Number=CardNum).count() == 0)
			self.Atm_Card_Number = CardNum
		super(AtmCard, self).save()


class AtMachine(models.Model):
	At_Machine_UID = models.AutoField(primary_key = True)
	Current_Balance = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	Location = models.CharField(max_length=100)
	MinimumBalance = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	Status = models.CharField(max_length=50)
	Last_Refill_Date = models.DateField()
	Next_Maintenance_Date = models.DateField()

class ATMachineRefill(models.Model):
	Refill_ID = models.AutoField(primary_key = True)
	At_Machine_UID = models.ForeignKey(AtMachine, on_delete=models.PROTECT)
	Amount = models.DecimalField(max_digits=25,decimal_places=0,default=0)
	ATM_Branch = models.CharField(max_length=100)
	Refill_Date = models.DateField()
	Previous_Balance = models.DecimalField(max_digits=25,decimal_places=0,default=0)

class Transaction(models.Model):
	Transaction_ID = models.AutoField(primary_key=True)
	ATM_Card_Number = models.ForeignKey(AtmCard, on_delete=models.PROTECT)
	Date = models.DateField()
	At_Machine_UID = models.ForeignKey(AtMachine, on_delete=models.PROTECT)
	Status = models.CharField(max_length=50)
	Response_Code = models.CharField(max_length=256)
	Type_Of_Transaction = models.CharField(max_length=50)


class Phone_Change(models.Model):
	Transaction_ID = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, db_column='Transaction_ID', parent_link=True)
	New_Phone_Number = models.CharField(max_length=20, default='0')

class Pin_Change(models.Model):
	Transaction_ID = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, db_column='Transaction_ID', parent_link=True)
	Previous_Pin = models.IntegerField()
	New_Pin = models.IntegerField()

class Cash_Withdrawal(models.Model):
	Transaction_ID = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, db_column='Transaction_ID', parent_link=True)
	Amount_Transferred = models.DecimalField(max_digits=25, decimal_places=2,default=0)
	Denomination = models.CharField(max_length=20, default='USD')
	Current_Balance = models.DecimalField(max_digits=20, decimal_places=10, default=0)

class Cash_Transfer(models.Model):
	Transaction_ID = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, db_column='Transaction_ID', parent_link=True)
	Beneficiary_Account_Number = models.IntegerField()
	Beneficiary_Name = models.CharField(max_length=60)
	Amout_Transferred = models.DecimalField(max_digits=25, decimal_places=2,default=0)

class Balance_Enquiry(models.Model):
	Transaction_ID = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True, db_column='Transaction_ID', parent_link=True)
	Balance_Amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)

#custom user creation
class UserManager(BaseUserManager):
	#creates standard user with requred information
	def create_user(self, username, password=None, is_staff=False, is_admin=False, is_active=True):
		if not username:
			raise ValueError("Users must have a username")
		if not password:
			raise ValueError("Users must have a password")
		userObj = self.model(
			username=username
		)
		userObj.set_password(password)
		userObj.staff = is_staff
		userObj.admin = is_admin
		userObj.active = is_active
		userObj.save(using=self._db)
		return userObj
	#creates user with staff prermissions
	def create_staffuser(self, username, password=None):
		user = self.create_user(
			username,
			password=password,
			is_staff=True
		)

		return user
	#creates user with Admin permissions
	def create_superuser(self, username, password=None):
		user = self.create_user(
			username,
			password=password,
			is_staff=True,
			is_admin=True
		)
		return user

#sets custom userprofile and requred information
class User(AbstractBaseUser):
	username = models.CharField(max_length=20, unique=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False) # a dmin user; non super-user
	admin = models.BooleanField(default=False) # a superuser
	Account_Number = models.ForeignKey(AccountExtension, on_delete=models.PROTECT, blank=True, null=True)
	USERNAME_FIELD = 'username'
	#username and password are required by default

	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.username

	def get_full_name(self):
		return self.username
	
	def get_short_name(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return True
	
	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff
	
	@property
	def is_admin(self):
		return self.admin
	
	@property
	def is_active(self):
		return self.active
	
	
