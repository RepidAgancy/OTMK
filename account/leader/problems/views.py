from rest_framework import views, generics, status
from rest_framework.response import Response

from account.leader.problems import serializers
from account import models, permissions, pagination


class ProblemsApiView(generics.ListAPIView):
    permission_classes = (permissions.IsLeader,)
    queryset = models.Problem.objects.all()
    serializer_class = serializers.LeaderProblemsSerializer
    pagination_class = pagination.CustomPagination
