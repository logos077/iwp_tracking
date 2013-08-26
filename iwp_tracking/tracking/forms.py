#forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import model_to_dict
from datetime import date, datetime, timedelta
from tracking.models import *

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield



class NewProjectForm(ModelForm):
    class Meta:
        model = Project
class NewWOForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = WorkOrder
class NewDriverForm(ModelForm):
    class Meta:
        model = Driver

class NewInstallerForm(ModelForm):
    class Meta:
        model = Installer

class NewContractorForm(ModelForm):
    class Meta:
        model = Contractor