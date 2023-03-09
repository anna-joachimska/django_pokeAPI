from rest_framework.pagination import LimitOffsetPagination
from .models import Type
from .serializers import TypeSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from pokemon.models import Pokemon


class TypeView(generics.GenericAPIView):
    serializer_class = TypeSerializer

    def get(self, request):
        types = Type.objects.all().values()
        if len(request.query_params) == 0:
            total_types = types.count()
            return Response({"status": status.HTTP_200_OK, "total": total_types, "data": types, })
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(types, request)
        serializer = TypeSerializer(result_page, many=True, context={'request': request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def get_type(self, name):
        try:
            return Type.objects.get(name=name)
        except:
            return None

    def post(self, request):
        type = self.get_type(request.data['name'])
        if type:
            return Response({"status": "fail", "message": f"type with '{request.data['name']}' name already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "type": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TypeDetail(generics.GenericAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def get_type(self, pk):
        try:
            return Type.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        type = self.get_type(pk=pk)
        if type is None:
            return Response({"status": "fail", "message": f"Type with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(type)
        return Response({"status": "success", "type": serializer.data})

    def patch(self, request, pk):
        type = self.get_type(pk)
        if type is None:
            return Response({"status": "fail", "message": f"Type with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "type": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        type = self.get_type(pk)
        if type is None:
            return Response({"status": "fail", "message": f"Type with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if len(Pokemon.types.through.objects.filter(type_id=pk)) > 0:
            return Response({"status": "fail", "message": f"Cannot delete type if pokemon has it"},
                            status=status.HTTP_400_BAD_REQUEST)
        type.delete()
        return Response({"status": "success", "message": "type deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
