from rest_framework.pagination import LimitOffsetPagination
from .models import Ability
from .serializers import AbilitySerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from pokemon.models import Pokemon


class AbilityView(generics.GenericAPIView):
    serializer_class = AbilitySerializer

    def get(self, request):
        abilities = Ability.objects.all().values()
        if len(request.query_params) == 0:
            total_abilities = abilities.count()
            return Response({"status": status.HTTP_200_OK, "total": total_abilities, "data": abilities, })
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(abilities, request)
        serializer = AbilitySerializer(result_page, many=True, context={'request': request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def get_ability(self, name):
        try:
            return Ability.objects.get(name=name)
        except:
            return None

    def post(self, request):
        ability = self.get_ability(request.data['name'])
        if ability:
            return Response({"status": "fail", "message": f"ability with '{request.data['name']}' name already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "ability": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AbilityDetail(generics.GenericAPIView):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer

    def get_ability(self, pk):
        try:
            return Ability.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        ability = self.get_ability(pk=pk)
        if ability is None:
            return Response({"status": "fail", "message": f"Ability with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(ability)
        return Response({"status": "success", "ability": serializer.data})

    def patch(self, request, pk):
        ability = self.get_ability(pk)
        if ability is None:
            return Response({"status": "fail", "message": f"Ability with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(ability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "ability": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ability = self.get_ability(pk)
        if ability is None:
            return Response({"status": "fail", "message": f"Ability with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if len(Pokemon.abilities.through.objects.filter(ability_id=pk)) > 0:
            return Response({"status": "fail", "message": f"Cannot delete ability if pokemon has it"},
                            status=status.HTTP_400_BAD_REQUEST)
        ability.delete()
        return Response({"status": "success", "message": "ability deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
