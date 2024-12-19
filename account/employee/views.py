from datetime import timedelta, datetime

from django.utils import timezone
from rest_framework import views, generics, status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from account import permissions, models, pagination
from account.employee import serializers


class MyProblemsApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsEmployee,)
    serializer_class = serializers.GetDateSerializer
    pagination_class = pagination.CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY,
                description='Sahifa raqamini kiriting',
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY,
                description='Sahifa hajmini belginlang',
                type=openapi.TYPE_NUMBER
            ),
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        start_date = serializer.validated_data.get('start_date', (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d"))
        end_date = serializer.validated_data.get('end_date', timezone.now().date())
        problems = models.Problem.objects.filter(employee__id=request.user.id, created_at__date__range=(start_date, end_date))
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(problems, request)
        if page is not None:
            serializer = serializers.MyProblemsSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializers.MyProblemsSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendProblemApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsEmployee,)
    serializer_class = serializers.SendProblemSerializer

    def post(self, request):
        serializer = serializers.SendProblemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Problem is successfully created"}, status=status.HTTP_201_CREATED)


class CheckProblemSolvedApiView(views.APIView):
    permission_classes = (permissions.IsEmployee,)

    def post(self, request, problem_id):
        try:
            problem = models.Problem.objects.get(id=problem_id, employee=request.user, programmer_is_solve=True)
        except models.Problem.DoesNotExist:
            return Response({"message": 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)
        problem.is_solved = True
        problem.save()
        return Response({'message': 'Problem successfully solved'}, status=status.HTTP_200_OK)


class GetSolvedProblemsApiView(views.APIView):
    permission_classes = (permissions.IsEmployee,)

    def get(self, request):
        employee = request.user
        problems = models.Problem.objects.filter(employee=employee, programmer_is_solve=True)
        serializer = serializers.MyProblemsSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)