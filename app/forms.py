# from django.forms import ModelForm
from django.forms.models import ModelForm
from django.forms import HiddenInput
from .models import CriminalRecord


class CriminalRecordForm(ModelForm):
    class Meta:
        model = CriminalRecord
        fields = ['offense', 'case_number', 'case_status', 'committed_at']
        widgets = {'user': HiddenInput()}
