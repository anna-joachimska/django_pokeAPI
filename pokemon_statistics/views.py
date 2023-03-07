from django.db import connection
from pokemon.models import Pokemon
from type.models import Type
from ability.models import Ability
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Count, Avg


class TypeWithHigestAvgHp(generics.GenericAPIView):

    def get(self, request):
        data = Type.objects.values('id', 'name').annotate(avg_hp=Avg('pokemon__hp')).order_by('-avg_hp')[0]
        return Response(data, status=status.HTTP_200_OK)


class TypeWithHigestAvgAttack(generics.GenericAPIView):

    def get(self, request):
        data = Type.objects.values('id', 'name').annotate(avg_attack=Avg('pokemon__attack')).order_by('-avg_attack')[0]
        return Response(data, status=status.HTTP_200_OK)


class TypeWithHigestAvgDefense(generics.GenericAPIView):

    def get(self, request):
        data = Type.objects.values('id', 'name').annotate(avg_defense=Avg('pokemon__defense')).order_by('-avg_defense')[
            0]
        return Response(data, status=status.HTTP_200_OK)


class CountPokemonsWithMoreThanXType(generics.GenericAPIView):

    def get(self, request, X):
        data = Pokemon.objects.filter(types__gt=X).annotate(pokemons=Count('types')).values().count()
        return Response({"pokemons_count": data}, status=status.HTTP_200_OK)


class MostPopularType(generics.GenericAPIView):

    def get(self, request):
        data = Type.objects.annotate(pokemon_count=Count('pokemon')).values('id', 'name').order_by('-pokemon_count')[0]
        return Response(data, status=status.HTTP_200_OK)


class MostPopularTypeWithPokemons(generics.GenericAPIView):

    def get(self, request):
        data = Type.objects.values('id', 'name').annotate(pokemon_count=Count('pokemon')).order_by('-pokemon_count')[0]
        return Response(data, status=status.HTTP_200_OK)


class PokemonTypesCount(generics.GenericAPIView):

    def get(self, request, pk):
        data = Type.objects.filter(id=pk).annotate(pokemons=Count('pokemon')).values('name', 'id', 'pokemons')
        return Response(data, status=status.HTTP_200_OK)


class AbilityWithHigestAvgHp(generics.GenericAPIView):

    def get(self, request):
        data = Ability.objects.values('id', 'name').annotate(avg_hp=Avg('pokemon__hp')).order_by('-avg_hp')[0]
        return Response(data, status=status.HTTP_200_OK)


class AbilityWithHigestAvgAttack(generics.GenericAPIView):

    def get(self, request):
        data = Ability.objects.values('id', 'name').annotate(avg_attack=Avg('pokemon__attack')).order_by('-avg_attack')[
            0]
        return Response(data, status=status.HTTP_200_OK)


class AbilityWithHigestAvgDefense(generics.GenericAPIView):

    def get(self, request):
        data = \
            Ability.objects.values('id', 'name').annotate(avg_defense=Avg('pokemon__defense')).order_by('-avg_defense')[
                0]
        return Response(data, status=status.HTTP_200_OK)


class CountPokemonsWithMoreThanXAbility(generics.GenericAPIView):

    def get(self, request, X):
        data = Pokemon.objects.filter(abilities__gt=X).annotate(pokemons=Count('abilities')).values().count()
        return Response({"pokemons_count": data}, status=status.HTTP_200_OK)


class MostPopularAbility(generics.GenericAPIView):

    def get(self, request):
        data = Ability.objects.annotate(pokemon_count=Count('pokemon')).values('id', 'name').order_by('-pokemon_count')[
            0]
        return Response(data, status=status.HTTP_200_OK)


class MostPopularAbilityWithPokemons(generics.GenericAPIView):

    def get(self, request):
        data = Ability.objects.values('id', 'name').annotate(pokemon_count=Count('pokemon')).order_by('-pokemon_count')[
            0]
        return Response(data, status=status.HTTP_200_OK)


class PokemonAbilitiesCount(generics.GenericAPIView):

    def get(self, request, pk):
        data = Ability.objects.filter(id=pk).annotate(pokemons=Count('pokemon')).values('name', 'id', 'pokemons')
        return Response(data, status=status.HTTP_200_OK)
