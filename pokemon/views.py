from .models import Pokemon
from .serializers import PokemonSerializer
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework import status
from .pagination import CustomPagination
from rest_framework.pagination import LimitOffsetPagination


class PokemonView(generics.GenericAPIView):

    serializer_class = PokemonSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request):
        pokemons = Pokemon.objects.all().values()
        total_pokemons = pokemons.count()
        return Response({"status":"success","total":total_pokemons, "data":pokemons},status=status.HTTP_200_OK)

    def get_pokemon(self, name):
        try:
            return Pokemon.objects.get(name=name)
        except:
            return None

    def post(self, request):
        print(request.data)
        pokemon = self.get_pokemon(request.data['name'])
        if pokemon:
            return Response({"status":"fail", "message":f"pokemon with '{request.data['name']}' name already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if not (request.data):
            raise serializers.ValidationError({"message": "You must pass a data to create a Pokemon"})

        serializer = self.serializer_class(data=request.data)

        if len(serializer.initial_data['name'])<0 or len(serializer.initial_data['generation'])<0:
            return Response({"status":"fail", "message":"data to create pokemon cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.initial_data['hp']<0 or serializer.initial_data['attack']<0 or serializer.initial_data['defense']<0:
            return Response({"status": "fail", "message": "invalid integer data"},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "pokemon": serializer.data}, status=status.HTTP_201_CREATED)
        else:
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
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})

    def patch(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)
        print(serializer.initial_data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        pokemon.delete()
        return Response({"status":"success", "message":"pokemon deleted successfully"},status=status.HTTP_204_NO_CONTENT)

class PokemonType(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def get_pokemon(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        pokemon = self.get_pokemon(pk=pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})

    def post(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        for i in range(0, len(request.data['types'])):
            if pokemon.types.filter(pk=request.data['types'][i]).exists():

                return Response({"status": "fail", "message": "this pokemon already has this type"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif pokemon.types.count()>=2:
                return Response({"status": "fail", "message": "this pokemon already has 2 types"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                pokemon.types.add(request.data['types'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "types added succesfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        for i in range(0, len(request.data['types'])):
            if not pokemon.types.filter(pk=request.data['types'][i]).exists():
                return Response({"status": "fail", "message": "this pokemon hasn't this type"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                pokemon.types.remove(request.data['types'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "types deleted succesfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PokemonAbility(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def get_pokemon(self, pk):
        try:
            return Pokemon.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        pokemon = self.get_pokemon(pk=pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon)
        return Response({"status": "success", "pokemon": serializer.data})


    def post(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        for i in range(0, len(request.data['abilities'])):
            if pokemon.abilities.filter(pk=request.data['abilities'][i]).exists():
                return Response({"status": "fail", "message": "this pokemon already has this ability"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif pokemon.abilities.count()>=3:
                return Response({"status": "fail", "message": "this pokemon already has 3 abilities"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                pokemon.abilities.add(request.data['abilities'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "abilities added succesfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pokemon = self.get_pokemon(pk)
        if pokemon == None:
            return Response({"status": "fail", "message": f"Pokemon with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(pokemon, data=request.data, partial=True)

        for i in range(0, len(request.data['types'])):
            if not pokemon.abilities.filter(pk=request.data['abilities'][i]).exists():
                return Response({"status": "fail", "message": "this pokemon hasn't this ability"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                pokemon.abilities.remove(request.data['abilities'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "abilities deleted succesfully", "pokemon": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

