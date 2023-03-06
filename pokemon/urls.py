from django.urls import path
from .views import PokemonView, PokemonDetail, AddOrRemoveTypeToPokemon, AddOrRemoveAbilityFromPokemon

urlpatterns = [
    path('', PokemonView.as_view()),
    path('<int:pk>', PokemonDetail.as_view()),
    path('add-or-remove-types/<int:pk>', AddOrRemoveTypeToPokemon.as_view()),
    path('add-or-remove-abilities/<int:pk>', AddOrRemoveAbilityFromPokemon.as_view()),
]
