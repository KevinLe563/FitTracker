import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from weightlog.models import Weight

class WeightForm(forms.ModelForm):
    class Meta:
        model = Weight
        fields = ['kg']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WeightForm, self).__init__(*args, **kwargs) 

    def clean_kg(self):
        data = self.cleaned_data['kg']
        if data < 0:
            raise ValidationError(_('Invalid weight -  This value must be positive!'))

        return data
    # remove option for user to edit the weight, can only log weight for
    # current day
    # def clean_date(self):
    #     data = self.cleaned_data['date']
    #     user_weights = Weight.objects.filter(date=data).filter(user=self.user)

    #     # Make sure this is a unique date
    #     if user_weights.exists():
    #         raise ValidationError(_('Invalid date -  A log for this date already exists'))

    #     if data > datetime.date.today():
    #         raise ValidationError(_('Invalid date - log in future'))

    #     return data

class UpdateWeightForm(forms.ModelForm):
    class Meta:
        model = Weight
        fields = ['kg']

    def clean_kg(self):
        data = self.cleaned_data['kg']
        if data < 0:
            raise ValidationError(_('Invalid weight -  This value must be positive!'))

        return data
        
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    username = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        
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