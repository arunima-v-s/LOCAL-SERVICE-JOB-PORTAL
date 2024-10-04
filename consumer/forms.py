from django import forms
from django.contrib.auth.models import User
from . import models

class ConsumerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets= {
            'password':forms.PasswordInput()
        }

class ConsumerForm(forms.ModelForm):
    class Meta:
        model=models.Consumer
        fields=['profile_pic','phone','city']

class AddressForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    mobile = forms.CharField(max_length=10, required=True)  # Change to CharField
    address = forms.CharField(max_length=500, required=True)