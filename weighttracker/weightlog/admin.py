from csv import list_dialects
from django.contrib import admin
from .models import Weight

# Register your models here.
@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'kg')
