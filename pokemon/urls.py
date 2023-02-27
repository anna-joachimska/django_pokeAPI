from django.urls import path
from .views import PokemonView, PokemonDetail, PokemonType, PokemonAbility

urlpatterns = [
    path('', PokemonView.as_view()),
    path('<int:pk>', PokemonDetail.as_view()),
    path('add-types/<int:pk>', PokemonType.as_view()),
    path('add-abilities/<int:pk>', PokemonAbility.as_view()),
]