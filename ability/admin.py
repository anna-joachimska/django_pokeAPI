from django.contrib import admin
from .models import Ability


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
