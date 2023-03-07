from django.urls import path
from .views import TypeWithHigestAvgHp, TypeWithHigestAvgAttack, TypeWithHigestAvgDefense, \
    PokemonTypesCount, MostPopularType, MostPopularTypeWithPokemons, CountPokemonsWithMoreThanXType, \
    AbilityWithHigestAvgHp, AbilityWithHigestAvgAttack, AbilityWithHigestAvgDefense, CountPokemonsWithMoreThanXAbility, \
    MostPopularAbility, MostPopularAbilityWithPokemons, PokemonAbilitiesCount

urlpatterns = [
    path('type/with-higest-hp', TypeWithHigestAvgHp.as_view()),
    path('type/with-higest-attack', TypeWithHigestAvgAttack.as_view()),
    path('type/with-higest-defense', TypeWithHigestAvgDefense.as_view()),
    path('type/count-pokemons/<int:pk>', PokemonTypesCount.as_view()),
    path('type/most-popular', MostPopularType.as_view()),
    path('type/most-popular-with-pokemons', MostPopularTypeWithPokemons.as_view()),
    path('type/count-pokemons-with-more-than-<int:X>-types', CountPokemonsWithMoreThanXType.as_view()),
    path('ability/with-higest-hp', AbilityWithHigestAvgHp.as_view()),
    path('ability/with-higest-attack', AbilityWithHigestAvgAttack.as_view()),
    path('ability/with-higest-defense', AbilityWithHigestAvgDefense.as_view()),
    path('ability/count-pokemons/<int:pk>', PokemonAbilitiesCount.as_view()),
    path('ability/most-popular', MostPopularAbility.as_view()),
    path('ability/most-popular-with-pokemons', MostPopularAbilityWithPokemons.as_view()),
    path('ability/count-pokemons-with-more-than-<int:X>-abilities', CountPokemonsWithMoreThanXAbility.as_view()),
]
