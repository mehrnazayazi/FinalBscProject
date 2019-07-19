from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BankAccount

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class AddAccoutForm(forms.ModelForm):
    cardNum = forms.CharField(max_length=20, required=True, help_text='')
    ExpirationDate = forms.DateField()
    name = forms.CharField(max_length=200, required=False, help_text='add a name to your card')

    class Meta:
        model = BankAccount
        fields = ('CardNum', 'ExpirationDate', 'name',)


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class RegisterForm(forms.Form):
    class Meta:
        model = User
        fields = ('Username', 'passWord', 'email')

# class DirectTransferForm(forms.Form):
