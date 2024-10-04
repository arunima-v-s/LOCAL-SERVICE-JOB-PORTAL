from django import forms
from django.contrib.auth.models import User
from . import models


class WorkerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','username','password']
        widgets = {
            'password':forms.PasswordInput()
        }

class WorkerForm(forms.ModelForm):
    class Meta:
        model=models.Worker
        fields=['phone','skills','work_experience','city','service_rate','profile_pic']

class ServiceForm(forms.ModelForm):
    class Meta:
        model=models.Services
        fields=['service_pic','skills','city','service_rate','phone']