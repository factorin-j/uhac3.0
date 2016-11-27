from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from .models import CriminalRecord, User
from django.forms import DateInput


class CriminalRecordForm(ModelForm):
    class Meta:
        model = CriminalRecord
        fields = ['user', 'offense', 'case_number', 'case_status', 'committed_at']
        widgets = {'committed_at': DateInput(attrs={'type': 'datetime'})}


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']
