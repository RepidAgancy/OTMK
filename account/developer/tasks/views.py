from rest_framework import views, status, generics, parsers
from rest_framework.response import Response

from account.developer.tasks import serializers
from account import models, permissions


class TasksApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer, )

    def get(self, request):
        boards = models.Board.objects.filter(tasks__programmers=self.request.user).distinct()
        serializer = serializers.BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTaskApiView(generics.UpdateAPIView):
    permission_classes = (permissions.IsProgrammer,)
    serializer_class = serializers.TaskUpdateSerializer
    queryset = models.Task
    parser_classes = [parsers.JSONParser]
    lookup_field = 'id'



class BoardsApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer, )
    def get(self, request):
        boards = models.Board.objects.all()
        boards_serializer = serializers.BoardSerializer(boards, many=True)
        return Response(boards_serializer.data, status=status.HTTP_200_OK)

