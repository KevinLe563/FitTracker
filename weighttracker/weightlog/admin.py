from django.contrib import admin
from .models import Weight

# Register your models here.
@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    pass
