from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .functions import IspayOk
from .forms import SignUpForm, AddAccoutForm
from .models import BankAccount, Profile


DefaultDestCard = 12345678
DefaultPassWord = 1234
DefaultCVV2 = 123
DefaultExdate = "12/12/1212"


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})
    else:
        return redirect('home')


def addAccount(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # accounts = BankAccount.objects.filter(User__username=request.user.username)
            # accounts = BankAccount.objects.all()
            # print(accounts)
            form = AddAccoutForm(request.POST)
            print(form.errors)
            if form.is_valid():
                account = form.save(commit=False)
                CardNum = form.cleaned_data.get('cardNum')
                accounts = BankAccount.objects.filter(User__username=request.user.username)
                for account in accounts:
                    if account.CardNum == CardNum:
                        return redirect('home')
                account.User = request.user
                name = form.cleaned_data.get('name')
                CardNum = form.cleaned_data.get('cardNum')
                ExpirationDate = form.cleaned_data.get('ExpirationDate')
                print(ExpirationDate)
                print(accounts)
                account.save()
                print(account)
                return redirect('home')

        else:
            form = AddAccoutForm()
            return render(request, 'blog/addaccount.html', {'form': form})
    return redirect('home')


def directTranfer(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            accounts = BankAccount.objects.filter(User__username=request.user.username)
            args = {'accounts': accounts}
            return render(request, 'blog/DirectTransfer.html', args)

        else:
            #TODO if split was 1 only
            cardNum = int(request.POST['choose account'].split()[1])
            password = int(request.POST.get("password"))
            cvv2 = int(request.POST.get("cvv2"))
            exdate = BankAccount.objects.get(CardNum=cardNum).ExpirationDate
            amount = int(request.POST.get("amount"))
            dest_card_num = request.POST.get("destcardnum")
            pay_is_ok = IspayOk(cardNum, password, cvv2, exdate, dest_card_num, amount)
            if pay_is_ok:
                return render(request, 'blog/successfulpay.html')
            return render(request, 'blog/failedpay.html')
    return redirect('home')


def addcredit(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            accounts = BankAccount.objects.filter(User__username=request.user.username)
            args = {'accounts': accounts}
            return render(request, 'blog/addcredit.html', args)
        else:
            #TODO if split was 1 only
            cardNum = int(request.POST['choose account'].split()[1])
            password = int(request.POST.get("password"))
            cvv2 = int(request.POST.get("cvv2"))
            print(request.POST.get("amount"))
            amount = int(request.POST.get("amount"))
            exdate = BankAccount.objects.get(CardNum=cardNum).ExpirationDate
            pay_is_ok = IspayOk(cardNum, password, cvv2, exdate, DefaultDestCard, amount)
            if pay_is_ok:
                credit = Profile.objects.get(user__username=request.user.username).credit
                credit = credit + amount
                Profile.objects.filter(user__username=request.user.username).update(credit=credit)
                print(credit)
                return render(request, 'blog/successfulpay.html')
            return render(request, 'blog/failedpay.html')
    return redirect('home')


def pay_with_credit(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            accounts = BankAccount.objects.filter(User__username=request.user.username)
            args = {'accounts': accounts}
            return render(request, 'blog/credittransfer.html', args)
        else:
            # TODO if split was 1 only
            amount = int(request.POST.get("amount"))
            credit = Profile.objects.get(user__username=request.user.username).credit
            if credit < amount:
                return render(request, 'blog/failedpay.html')
            dest_card_num = request.POST.get("destcardnum")
            pay_is_ok = IspayOk(DefaultDestCard, DefaultPassWord, DefaultCVV2, DefaultExdate,
                                dest_card_num, amount)
            if pay_is_ok:
                credit = credit - amount
                Profile.objects.filter(user__username=request.user.username).update(credit=credit)
                return render(request, 'blog/successfulpay.html')
            return render(request, 'blog/failedpay.html')
    return redirect('home')


def home(request):
    context = {

    }
    return render(request, 'blog/home.html',context)


def about(request):
    return render(request, 'blog/about.html')

