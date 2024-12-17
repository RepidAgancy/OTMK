from datetime import datetime, timedelta

from django.db.models import F, Count
from rest_framework import views, generics, status
from rest_framework.response import Response

from account.leader.dashboard import serializers
from account import models, permissions


class StatisticsApiView(generics.GenericAPIView):
    serializer_class = serializers.DashboardGetDateSerializer
    permission_classes = (permissions.IsLeader,)

    def post(self, request):
        serializer = serializers.DashboardGetDateSerializer(data=request.data)
        serializer.is_valid()
        start_date = serializer.validated_data.get('start_date', (datetime.now().date() - timedelta(days=365)))
        end_date = serializer.validated_data.get('end_date', datetime.now().date())
        problems = models.Problem.objects.filter(created_at__date__range=(start_date, end_date))
        solved_problems = problems.filter(is_solved=True)
        not_solved_problems = problems.filter(is_solved=False)
        data = {
            'problems': problems.count(),
            'problems_solved': solved_problems.count(),
            'problems_not_solved': not_solved_problems.count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class AllProblemsApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request):
        problems = models.Problem.objects.all()
        solved_problems = models.Problem.objects.filter(is_solved=True)
        not_solved_problems = models.Problem.objects.filter(is_solved=False)
        data = {
            'problems': problems.count(),
            'solved_problems': solved_problems.count(),
            'not_solved_problems': not_solved_problems.count()
        }
        return Response(data, status=status.HTTP_200_OK)


class MonthlyStatisticsApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request):
        problems = models.Problem.objects.filter(is_solved=True).annotate(
            month=F('created_at__month')
        ).values('month').annotate(count=Count('id')).order_by('month')

        data = {month: 0 for month in range(1, 13)}
        for problem in problems:
            data[problem['month']] = problem['count']

        return Response(data, status=status.HTTP_200_OK)


class ProblemsApiView(views.APIView):
    permission_classes = (permissions.IsLeader,)

    def get(self, request):
        problems = models.Problem.objects.filter(created_at__date=datetime.now().date())[:6]
        serializer = serializers.ProblemsSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)