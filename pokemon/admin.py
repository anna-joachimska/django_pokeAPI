from django.contrib import admin
from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['types', 'abilities', 'generation', 'hp', 'attack', 'defense', 'name']
