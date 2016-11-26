# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.forms import HiddenInput
from .models import User, Account


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class AccountCreateForm(ModelForm):
    class Meta:
        model = Account
        fields = ['user', 'account_name', 'account_number']
        widgets = {'user': HiddenInput()}
