from django import forms
from .models import *

class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username','name':'username','required':True}),
        label='',
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password','name':'password','required':True}),
        label='',
    )
    class Meta:
        model = Register
        fields=['username','password']
       