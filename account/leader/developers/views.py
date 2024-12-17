from datetime import datetime, timedelta

from rest_framework import views, generics, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from account.leader.developers import serializers, filters
from account import models, permissions, pagination


class ProgrammersApiView(generics.ListAPIView):
    permission_classes = (permissions.IsLeader, )
    serializer_class = serializers.ProgrammersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProgrammerProblemFilterByProblemSolveTimeFilter

    def get_queryset(self):
        return models.User.objects.filter(role=models.PROGRAMMER)


class ProgrammerSolvedProblemsApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.ProgrammerGetDateSerializer
    pagination_class = pagination.CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY,
                description="Sahifa raqamini kiriting",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY,
                description="Sahifa hajmini kiriting",
                type=openapi.TYPE_NUMBER,
            )
        ]
    )
    def post(self, request, developer_id):
        try:
            developer = models.User.objects.get(id=developer_id, role=models.PROGRAMMER)
        except models.User.DoesNotExist:
            return Response({"message": "developer not found"}, status=status.HTTP_404_NOT_FOUND)
        problems = models.Problem.objects.filter(programmer=developer, programmer_is_solve=True,)

        serializer = serializers.ProgrammerGetDateSerializer(data=request.data)
        serializer.is_valid()
        start_date = serializer.validated_data.get('start_date', None)
        end_date = serializer.validated_data.get('end_date', None)
        if start_date and end_date:
            problems = problems(
                created_at__date__range=(start_date, end_date)
            )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(problems, request)
        serializer = serializers.ProblemsSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeveloperKeepBusiesApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request, developer_id):
        try:
            developer = models.User.objects.get(role=models.PROGRAMMER, id=developer_id)
        except models.User.DoesNotExist:
            return Response({'message': 'Developer not found'}, status=status.HTTP_404_NOT_FOUND)
        keep_busies = models.KeepBusy.objects.filter(programmer=developer)
        serializer = serializers.KeepBusiesSerializer(keep_busies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeveloperAddApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsLeader,)
    serializer_class = serializers.DeveloperAddSerializer

    def post(self, request):
        serializer = serializers.DeveloperAddSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": 'User successfully added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)