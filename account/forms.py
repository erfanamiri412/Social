from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="password", widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="confirm password", widget = forms.PasswordInput(attrs={'class':'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            raise ValidationError('This username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!')
        return email
    
def clean(self):
    cleaned_data = super().clean()
    p1 = cleaned_data.get('password1')
    p2 = cleaned_data.get('password2')

    if p1 and p2 and p1 != p2:
        self.add_error('password2', 'Passwords do not match')
        
class UserLoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))