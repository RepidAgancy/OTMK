from rest_framework import views, status
from rest_framework.response import Response

from account.developer.tasks import serializers
from account import models, permissions


class TasksApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer, )

    def get(self, request):
        tasks = models.Task.objects.filter(programmers=request.user)
        serializer = serializers.TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
