import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from weightlog.models import Weight

class WeightForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today())
    class Meta:
        model = Weight
        fields = ['date', 'note', 'kg']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WeightForm, self).__init__(*args, **kwargs) 

    def clean_date(self):
        data = self.cleaned_data['date']
        user_weights = Weight.objects.filter(date=data).filter(user=self.user)

        # Make sure this is a unique date
        if user_weights.exists():
            raise ValidationError(_('Invalid date -  A log for this date already exists'))

        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - log in future'))

        return data