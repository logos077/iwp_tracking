#forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import model_to_dict
from datetime import date, datetime, timedelta
from tracking.models import *

class NewProjectForm(ModelForm):
    class Meta:
        model = Project
class NewWOForm(ModelForm):
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
        model = Installer