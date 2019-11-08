from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .processing import *
from . import forms
from . import models

def index(request):
	return render(request, "ATM/index.html")

def enquiry(request):
	return HttpResponse("This is the balance enquiry page.")

def withdraw(request):
	return HttpResponse("This is the cash withdrawal page.")

def transfer(request, Account_Number):
	t = models.Transaction(
			ATM_Card_Number=models.AtmCard.objects.get(Account_Number=Account_Number),
			Date = timezone.now(),
			At_Machine_UID = models.AtMachine.objects.get(At_Machine_UID=1),
			Status = "Unsucessful",
			Response_Code = "Unable to process",
			Type_Of_Transaction = "Cash Transfer"
		)
	t.save()

	if request.method == "POST":
		form = forms.CashTransForm(request.POST)
		if form.is_valid():
			form.Transaction_ID = t.Transaction_ID
			form.save()

			user_account = models.AccountExtension.objects.get(Account_Number=Account_Number)
			dest_account = models.AccountExtension.objects.get(Account_Number=form.Beneficiary_Account_Number)

			user_account.balance = user_account.balance - form.enter_trans_amount
			dest_account.balance = dest_account.balance + form.enter_trans_amount

			t.Status = "Sucessful"
			t.Response_Code = "Processed"
			t.save()

			user_account.save()
			dest_account.save()
		
		return redirect("ATM/index.html")

	else:
		form = forms.CashTransForm()

	return render(request, "ATM/cash_transfer.html", {"form": form})

def confirm(request):

	transType = request.POST['TransactionType']
	if transType=="Withdraw":
		message = processing.withdraw(request)
	elif transType == "Transfer":
		message = processing.transfer(request)
	elif transType == "Enquiry":
		message = processing.transfer(request)
	else:
		raise "Invalid transaction type"

	return HttpResponse(message)
