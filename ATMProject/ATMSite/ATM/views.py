from django.http import HttpResponse
from django.shortcuts import render
from .processing import *

def index(request):
	return HttpResponse ("This is the index page of the ATM app.")

def enquiry(request):
	return HttpResponse("This is the balance enquiry page.")

def withdraw(request):
	return HttpResponse("This is the cash withdrawal page.")

def transfer(request):
	return HttpResponse("This is the cash transfer page.")

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
