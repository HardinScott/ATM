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
    messages.info(request, request.user)
    messages.info(request, models.AccountExtension.objects.get(Account_Number=request.user.Account_Number).Balance)
    return redirect("ATM:homepage")

@login_required(login_url="/ATM/login/")
def withdraw(request):
    w = models.Transaction(
        ATM_Card_Number=models.AtmCard.objects.get(Account_Number=request.user.Account_Number),
        Date=timezone.now(),
        At_Machine_UID=models.AtMachine.objects.get(At_Machine_UID=1),
        Status="Unsucessful",
        Response_Code="Unable to process",
        Type_Of_Transaction="Withdrawal/"
    )
    w.save()

    if request.method == "POST":
        form = forms.CashWithdrawal(request.POST)
        if form.is_valid():
            form.Transaction_ID = w.Transaction_ID
            form.save()

            transfer_amount = form.cleaned_data.get('Amount_Transferred')
            user_acc = request.user.Account_Number  # get current user AccountExtension model
            if transfer_amount > user_acc.Balance:
                w.Status = "Failure"
                w.Response_Code = "Processed"
                w.save()
                messages.info(request, "Withdrawal Failed")
                return redirect("ATM:homepage")
            user_acc.Balance = user_acc.Balance - transfer_amount

            w.Status = "Successful"  # update ransaction status as sucesful
            w.Response_Code = "Processed"  # change Response code to processed
            w.save()  # save new information
            user_acc.save()

        messages.info(request, "Widthdrawl Successful")
        return redirect("ATM:homepage")

    else:
        form = forms.CashWithdrawal()

    return render(request, "ATM/withdraw.html", {"form": form})

def transfer(request):
    #gets information from CashTransForms
    if request.method == "POST":
        #check if user is authenticated if anon then use CashTransNotLoginForm for card and pin number
        if not request.user.is_authenticated:
            form = forms.CashTransNotLoginForm(request.POST)
        else:
            form = forms.CashTransForm(request.POST)
        
        #check if form is valid.
        if form.is_valid():
            #determine if user is logged in or needs to enter card and pin number
            if request.user.is_authenticated:
                try:
                    user_acc = request.user.Account_Number #get current user AccountExtension model
                except:
                    user_acc = None #account not found
            else:
                try:
                    atm_card = models.AtmCard.objects.get(Atm_Card_Number=form.cleaned_data.get('card_number')) #get Atmcard model for card number
                except:
                    atm_card = None #AtmCard not found
                pin_numb = form.cleaned_data.get('pin')

                if atm_card is None or atm_card.PIN != pin_numb:
                    messages.error(request, "Atm card number or pin not valid!")
                    return redirect("ATM:transfer")
                try:
                    user_acc = models.AccountExtension.objects.get(Account_Number=atm_card.Account_Number.Account_Number) #get Account Extension from atm card
                except:
                    user_acc = None
            if user_acc == None:
                messages.error(request, "Users account invalid!")
                return redirect("ATM: transfer")
            #creates new transaction and gets information
            t = models.Transaction(
                ATM_Card_Number=models.AtmCard.objects.get(Account_Number=user_acc.Account_Number),
                Date=timezone.now(),
                At_Machine_UID=models.AtMachine.objects.get(At_Machine_UID=getCurrentATM()),
                Status="Unsucessful",
                Response_Code="Unable to process",
                Type_Of_Transaction="Transfer"
            )
            t.save() #save tranaction with base info

            form.Transaction_ID = t.Transaction_ID #put trans id into transfer model
            form.save() #save Cash_Transfer model
            
            try:
                dest_acc = models.AccountExtension.objects.get(Account_Number=form.cleaned_data.get('Beneficiary_Account_Number')) #get destination Account Extension
            except:
                messages.error(request, "Beneficiary account number invalid!")
                return redirect("ATM:transfer")

            transfer_ammount = form.cleaned_data.get('Amout_Transferred') #get tranfer ammount from form

            user_acc.Balance = user_acc.Balance -  transfer_ammount #update user_acc balance with balance minus transfered ammount
            dest_acc.Balance = dest_acc.Balance - transfer_ammount #update dest_acc balance with balance minus transfered ammount

            t.Status = "Sucessful" #update ransaction status as sucesful
            t.Response_Code = "Processed" #change Response code to processed
            t.save() #save new information

            user_acc.save() #save new balance to user
            dest_acc.save()#save new balance to destination

        messages.info(request, "Transfer Successful!")
        return redirect("ATM:homepage")
    #if not POST request
    else:
        #check if user is authenticated if anon then use CashTransNotLoginForm for card and pin number
        if not request.user.is_authenticated:
            form = forms.CashTransNotLoginForm()
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

#Reads current UID for atm from ATM_UID.txt file in ATMSite directory
def getCurrentATM():
    f = open("ATM_UID.txt", "r")
    current_atm = f.readline()
    f.close()
    return int(current_atm)
