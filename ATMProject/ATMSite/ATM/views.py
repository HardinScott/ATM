from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import processing
from . import forms
from . import models

def homepage(request):
    return render(request, 'ATM/home.html')

def index(request):
    return render(request, "ATM/index.html")

@login_required(login_url="/ATM/login/") #ensures that user is logged in before allowing accessing page
def enquiry(request):
    return render(request, "ATM/balance.html")

@login_required(login_url="/ATM/login/")
def withdraw(request):
    return render(request, "ATM/withdraw.html")

@login_required(login_url="/ATM/login/")
def transfer(request):
    #creates new transaction and gets information
    t = models.Transaction(
        ATM_Card_Number=models.AtmCard.objects.get(Account_Number=request.user.Account_Number),
        Date=timezone.now(),
        At_Machine_UID=models.AtMachine.objects.get(At_Machine_UID=1),
        Status="Unsucessful",
        Response_Code="Unable to process",
        Type_Of_Transaction="Transfer"
    )
    t.save() #save tranaction with base info

    #gets information from CashTransForm
    if request.method == "POST":
        form = forms.CashTransForm(request.POST)
        #if valid get transaction id and save cash_transfer model
        if form.is_valid():
            form.Transaction_ID = t.Transaction_ID
            form.save()

            user_acc = request.user.Account_Number #get current user AccountExtension model
            dest_acc = models.AccountExtension.objects.get(Account_Number=form.cleaned_data.get('Beneficiary_Account_Number')) #get destination Account Extension

            transfer_ammount = form.cleaned_data.get('Amout_Transferred') #get tranfer ammount from form

            user_acc.Balance = user_acc.Balance -  transfer_ammount
            dest_acc.Balance = dest_acc.Balance - transfer_ammount

            t.Status = "Sucessful" #update ransaction status as sucesful
            t.Response_Code = "Processed" #change Response code to processed
            t.save() #save new information

            user_acc.save() #save new balance to user
            dest_acc.save()#save new balance to destination
        messages.info(request, "Transfer Successful!")
        return redirect("ATM:homepage", Transaction_ID=t.Transaction_ID)

    else:
        form = forms.CashTransForm()

    return render(request, "ATM/cash_transfer.html", {"form": form})

#Logout current user
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("ATM:homepage")

#login user 
def login_request(request):
    #get information from AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') #get username from form
            password = form.cleaned_data.get('password') #get pasword from form
            user = authenticate(username=username, password=password) #authenticate user
            if user is not None: #user authenticated
                login(request, user) #login user
                messages.info(request, f"You are now logged in as {username}") #diplays message using toast in header.html
                #check to see if login.html contain next in post reponse then reidirects to previouly requested page.
                if'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("ATM:homepage") #redirects user to home page
            else:
                messages.error(request, "Invalid username or password") #displays error message using toast in header.html
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm() #gets Authentication form 
    return render(request, "ATM/login.html", {"form":form}) #renders login page and form requests.