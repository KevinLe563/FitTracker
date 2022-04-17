from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

# Create your models here.

class Weight(models.Model):
    # Each weight is associated with a user
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=False)
    date = models.DateField(null=False, blank=False, auto_now=True)
    kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        """Represent weight object as a date"""
        return self.date
