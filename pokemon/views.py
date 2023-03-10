from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pokemon
from .serializers import PokemonSerializer, AddOrRemoveTypeFromPokemonSerializer, \
    AddOrRemoveAbilityFromPokemonSerializer
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination


class PokemonView(generics.GenericAPIView):
    queryset = Pokemon.objects.all().values()
    serializer_class = PokemonSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['id', 'name', 'hp', 'attack', 'defense', 'generation']
    ordering = ['id']

    def get(self, request):
        if len(request.query_params) == 0:
            pokemons = Pokemon.objects.all().values()
            total_pokemons = pokemons.count()
            return Response({"status": "success", "total": total_pokemons, "data": pokemons}, status=status.HTTP_200_OK)
        try:
            if request.query_params['ordering'] is not None:
                pokemons = Pokemon.objects.all().order_by(request.query_params['ordering']).values()
                return Response(pokemons)
        except MultiValueDictKeyError:
            pokemons = Pokemon.objects.all().values()
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(pokemons, request)
            serializer = PokemonSerializer(result_page, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_pokemon(self, name):
        try:
            return Pokemon.objects.get(name=name)
        except:
            return None

    def post(self, request):
        pokemon = self.get_pokemon(request.data['name'])
        if pokemon:
            return Response({"status": "fail", "message": f"pokemon with '{request.data['name']}' name already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "pokemon": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PokemonDetail(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def get_pokemon(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        pokemon = self.get_pokemon(pk=pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})

    def patch(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        pokemon.delete()
        return Response({"status": "success", "message": "pokemon deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class AddOrRemoveTypeToPokemon(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = AddOrRemoveTypeFromPokemonSerializer

    def get_pokemon(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        pokemon = self.get_pokemon(pk=pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})

    def post(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)
        if serializer.validate_add(data=request.data) and serializer.is_valid():
            new_types_list = []
            old_types_list = []
            for type in request.data['types']:
                if pokemon.types.filter(pk=type).exists():
                    old_types_list.append(type)
                else:
                    new_types_list.append(type)
            if len(old_types_list) > 0:
                return Response({"status": "fail", "message": "this pokemon already has this type",
                                 "existing_pokemon_types": old_types_list},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for type in new_types_list:
                    pokemon.types.add(type)

            return Response(
                {"status": "success", "message": "type added successfully", "pokemon": serializer.data})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        if serializer.is_valid():
            types_list = []
            old_types_list = []
            for type in request.data['types']:
                if not pokemon.types.filter(pk=type).exists():
                    types_list.append(type)
                else:
                    old_types_list.append(type)

            if len(types_list) > 0:
                return Response(
                    {"status": "fail", "message": "this pokemon hasn't this types", "types_to_remove": types_list,
                     "existing_types": old_types_list},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                for type in old_types_list:
                    pokemon.types.remove(type)

            return Response(
                {"status": "success", "message": "types deleted successfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddOrRemoveAbilityFromPokemon(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = AddOrRemoveAbilityFromPokemonSerializer

    def get_pokemon(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        pokemon = self.get_pokemon(pk=pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})

    def post(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)
        if serializer.validate_add(data=request.data) and serializer.is_valid():
            new_abilities_list = []
            old_abilities_list = []
            for ability in request.data['abilities']:
                if pokemon.abilities.filter(pk=ability).exists():
                    old_abilities_list.append(ability)
                else:
                    new_abilities_list.append(ability)
            if len(old_abilities_list) > 0:
                return Response({"status": "fail", "message": "this pokemon already has this abilities",
                                 "pokemon_abilities": old_abilities_list},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for ability in new_abilities_list:
                    pokemon.abilities.add(ability)

            return Response(
                {"status": "success", "message": "ability added successfully", "pokemon": serializer.data})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon is None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        if serializer.is_valid():
            abilities_list = []
            old_abilities_list = []
            for ability in request.data['abilities']:
                if not pokemon.abilities.filter(pk=ability).exists():
                    abilities_list.append(ability)
                else:
                    old_abilities_list.append(ability)

            if len(abilities_list) > 0:
                return Response({"status": "fail", "message": "this pokemon hasn't this abilities",
                                 "abilities_to_remove": abilities_list, "existing_abilities": old_abilities_list},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for ability in old_abilities_list:
                    pokemon.abilities.remove(ability)

            return Response(
                {"status": "success", "message": "ability deleted successfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
