# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.forms
from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# class AccountCreateForm()
