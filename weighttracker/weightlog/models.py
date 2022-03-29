from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Weight(models.Model):
    # Each weight is associated with a user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=False, blank=False)
    note = models.TextField(max_length=500, help_text="Personal notes")

    def __str__(self):
        """Represent weight object as a date"""
        return self.date
