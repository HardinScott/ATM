from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse ("This is the index page of the ATM app.")

def enquiry(request):
	return HttpResponse("This is the balance enquiry page.")

def withdraw(request):
	return HttpResponse("This is the cash withdrawal page.")

def transfer(request):
	return HttpResponse("This is the cash transfer page.")

def confirm(request):
	return HttpResponse("This is the transaction confirmation page.")
