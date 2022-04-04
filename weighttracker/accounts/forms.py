from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        
    def clean_username(self):
        fusername = self.cleaned_data['username']
        
        user_with_username = User.objects.filter(username=fusername)
        
        # Check if existing user has this username
        if user_with_username.exists():
            raise ValidationError(_('Account with this username already exists. Please try a different username.'))
        
        return fusername

    def clean_email(self):
        femail = self.cleaned_data['email']

        user_with_email = User.objects.filter(email=femail)
        
        # Check if existing user has this email
        if user_with_email.exists():
            raise ValidationError(_('Account with this email already exists. Please try a different email.'))
        
        return femail
