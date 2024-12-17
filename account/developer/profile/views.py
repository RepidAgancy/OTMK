from datetime import datetime, timedelta

from rest_framework import views, generics, status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from account.developer.profile import serializers
from account import models, permissions, pagination


class SolvedProblemsApiView(generics.GenericAPIView):
    serializer_class = serializers.ProfileGetDateSerializer
    permission_classes = (permissions.IsProgrammer,)
    pagination_class = pagination.CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY,
                description="Sahifa raqamini kiriting",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY,
                description="Sahifa hajmini kiriting",
                type=openapi.TYPE_NUMBER
            )
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        start_date = serializer.validated_data.get('start_date', (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d"))
        end_date = serializer.validated_data.get('end_date', (datetime.now()))
        problems = models.Problem.objects.filter(created_at__date__range=(start_date, end_date), programmer=request.user, programmer_is_solve=True)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(problems, request)
        if page is not None:
            serializer = serializers.ProfileSolveProblemsSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializers.ProfileSolveProblemsSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileKeepBusyApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer,)

    def get(self, request):
        programmer = request.user
        keep_busy = models.KeepBusy.objects.filter(programmer=programmer)
        serializer = serializers.ProfileKeepBusySerializer(keep_busy, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileApiView(generics.GenericAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsProgrammer,)

    def get(self, request):
        programmer = request.user
        serializer = serializers.ProfileSerializer(programmer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileChangeApiView(generics.GenericAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsProgrammer,)

    def patch(self, request):
        programmer = request.user
        serializer = serializers.ProfileSerializer(instance=programmer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile successfully updated"}, status=status.HTTP_200_OK)
        return Response({"message": "Something went wrong"})



