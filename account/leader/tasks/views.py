from rest_framework import generics, views, status, parsers
from rest_framework.response import Response

from account import models, permissions
from account.leader.tasks import serializers


class CreateBoardApiView(generics.CreateAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.CreateNewBoardSerializer
    queryset = models.Board


class CreateTaskApiView(generics.CreateAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.TaskSerializer
    queryset = models.Task
    parser_classes = [parsers.JSONParser]


class UpdateTaskApiView(generics.UpdateAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.TaskSerializer
    queryset = models.Task
    parser_classes = [parsers.JSONParser]
    lookup_field = 'id'


class GetTaskApiView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.GetTaskSerializer
    queryset = models.Task
    lookup_field = 'id'


class BoardApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request):
        board = models.Board.objects.all()
        serializer = serializers.BoardSerializer(board, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDeveloperListApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request):
        programmers = models.User.objects.filter(role=models.PROGRAMMER)
        serializer = serializers.ProgrammersListSerializer(programmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTaskApiView(generics.DestroyAPIView):
    permission_classes = (permissions.IsLeader,)
    queryset = models.Task
    lookup_field = 'id'


class DeleteBoardApiView(generics.DestroyAPIView):
    permission_classes = (permissions.IsLeader,)
    queryset = models.Board
    lookup_field = 'id'
