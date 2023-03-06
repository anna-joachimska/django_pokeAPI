from django.db import connection
from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer
from type.models import Type
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework import status
from django.db.models import Avg, Max, Count


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class TypeWithHigestAvgHp(generics.GenericAPIView):

    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.hp) AS average_hp, pokemon_pokemon_types.type_id AS id, type_type.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_types, type_type ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_types.pokemon_id ' \
                'AND pokemon_pokemon_types.type_id = type_type.id ' \
                'GROUP BY pokemon_pokemon_types.type_id, type_type.name ' \
                'ORDER BY average_hp desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class TypeWithHigestAvgAttack(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.attack) AS average_attack, pokemon_pokemon_types.type_id AS id, type_type.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_types, type_type ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_types.pokemon_id ' \
                'AND pokemon_pokemon_types.type_id = type_type.id ' \
                'GROUP BY pokemon_pokemon_types.type_id, type_type.name ' \
                'ORDER BY average_attack desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class TypeWithHigestAvgDefense(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.defense) AS average_defense, pokemon_pokemon_types.type_id AS id, type_type.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_types, type_type ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_types.pokemon_id ' \
                'AND pokemon_pokemon_types.type_id = type_type.id ' \
                'GROUP BY pokemon_pokemon_types.type_id, type_type.name ' \
                'ORDER BY average_defense desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class CountPokemonsWithMoreThanXType(generics.GenericAPIView):
    def get(self, request, X):
        data = Pokemon.objects.filter(types__gt=X).annotate(pokemons=Count('types')).values().count()
        return Response({"pokemons_count": data}, status=status.HTTP_200_OK)


class MostPopularType(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT id, name FROM ' \
                '(SELECT max("pokemon_count") as "max_count", id , name  ' \
                'FROM (SELECT count(pokemon_pokemon.id) AS pokemon_count, pokemon_pokemon_types.type_id ' \
                'FROM pokemon_pokemon_types, pokemon_pokemon ' \
                'WHERE pokemon_pokemon.id = pokemon_pokemon_types.pokemon_id ' \
                'GROUP BY pokemon_pokemon_types.type_id ' \
                'ORDER BY pokemon_count desc) most_popular_types, type_type ' \
                'WHERE type_type.id = most_popular_types.type_id ' \
                'GROUP BY type_id ' \
                'ORDER BY max_count desc ' \
                'LIMIT 1) most_popular_types ;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class MostPopularTypeWithPokemons(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT max("count") AS pokemons_count, id, name ' \
                'FROM (SELECT count(pokemon_pokemon.id) AS "count", pokemon_pokemon_types.type_id ' \
                'FROM pokemon_pokemon_types, pokemon_pokemon ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_types.pokemon_id ' \
                'GROUP BY pokemon_pokemon_types.type_id ' \
                'ORDER BY "count" desc) most_popular_types, type_type ' \
                'WHERE type_type.id = most_popular_types.type_id ' \
                'GROUP BY id ' \
                'ORDER BY "pokemons_count" desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class PokemonTypesCount(generics.GenericAPIView):
    serializer_class = PokemonSerializer

    def get(self, request):
        pokemons = Pokemon.types.through.objects.all().values()
        type_pokemons = pokemons.filter(type_id=request.data['type'])
        total_type_pokemons = type_pokemons.count()
        return Response({"status": "success", "total": total_type_pokemons, "data": type_pokemons},
                        status=status.HTTP_200_OK)


class AbilityWithHigestAvgHp(generics.GenericAPIView):

    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.hp) AS average_hp, pokemon_pokemon_abilities.ability_id AS id, ability_ability.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_abilities, ability_ability ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_abilities.pokemon_id ' \
                'AND pokemon_pokemon_abilities.ability_id = ability_ability.id ' \
                'GROUP BY pokemon_pokemon_abilities.ability_id, ability_ability.name ' \
                'ORDER BY average_hp desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class AbilityWithHigestAvgAttack(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.attack) AS average_attack, pokemon_pokemon_abilities.ability_id AS id, ability_ability.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_abilities, ability_ability ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_abilities.pokemon_id ' \
                'AND pokemon_pokemon_abilities.ability_id = ability_ability.id ' \
                'GROUP BY pokemon_pokemon_abilities.ability_id, ability_ability.name ' \
                'ORDER BY average_attack desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class AbilityWithHigestAvgDefense(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT AVG(pokemon_pokemon.defense) AS average_defense, pokemon_pokemon_abilities.ability_id AS id, ability_ability.name ' \
                'FROM pokemon_pokemon, pokemon_pokemon_abilities, ability_ability ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_abilities.pokemon_id ' \
                'AND pokemon_pokemon_abilities.ability_id = ability_ability.id ' \
                'GROUP BY pokemon_pokemon_abilities.ability_id, ability_ability.name ' \
                'ORDER BY average_defense desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class CountPokemonsWithMoreThanXAbility(generics.GenericAPIView):
    def get(self, request, X):
        data = Pokemon.objects.filter(abilities__gt=X).annotate(pokemons=Count('abilities')).values().count()
        return Response({"pokemons_count": data}, status=status.HTTP_200_OK)


class MostPopularAbility(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT id, name FROM ' \
                '(SELECT max("pokemon_count") as "max_count", id , name  ' \
                'FROM (SELECT count(pokemon_pokemon.id) AS pokemon_count, pokemon_pokemon_abilities.ability_id ' \
                'FROM pokemon_pokemon_abilities, pokemon_pokemon ' \
                'WHERE pokemon_pokemon.id = pokemon_pokemon_abilities.pokemon_id ' \
                'GROUP BY pokemon_pokemon_abilities.ability_id ' \
                'ORDER BY pokemon_count desc) most_popular_abilities, ability_ability ' \
                'WHERE ability_ability.id = most_popular_abilities.ability_id ' \
                'GROUP BY ability_id ' \
                'ORDER BY max_count desc ' \
                'LIMIT 1) most_popular_abilities ;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class MostPopularAbilityWithPokemons(generics.GenericAPIView):
    def get(self, request):
        query = 'SELECT max("count") AS pokemons_count, id, name ' \
                'FROM (SELECT count(pokemon_pokemon.id) AS "count", pokemon_pokemon_abilities.ability_id ' \
                'FROM pokemon_pokemon_abilities, pokemon_pokemon ' \
                'WHERE pokemon_pokemon.id=pokemon_pokemon_abilities.pokemon_id ' \
                'GROUP BY pokemon_pokemon_abilities.ability_id ' \
                'ORDER BY "count" desc) most_popular_abilities, ability_ability ' \
                'WHERE ability_ability.id = most_popular_abilities.ability_id ' \
                'GROUP BY id ' \
                'ORDER BY "pokemons_count" desc ' \
                'LIMIT 1;'
        cursor = connection.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        return Response(data, status=status.HTTP_200_OK)


class PokemonAbilitiesCount(generics.GenericAPIView):
    serializer_class = PokemonSerializer

    def get(self, request):
        pokemons = Pokemon.abilities.through.objects.all().values()
        ability_pokemons = pokemons.filter(ability_id=request.data['ability'])
        total_ability_pokemons = ability_pokemons.count()
        return Response({"status": "success", "total": total_ability_pokemons, "data": ability_pokemons},
                        status=status.HTTP_200_OK)
