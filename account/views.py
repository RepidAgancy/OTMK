from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account import models, serializers


class LoginApiView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserLogoutSerializer

    def post(self, request):
        try:
            refresh = request.data['refresh_token']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "User successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error occured {e}"})


class UserProfileApiView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        serializer = serializers.UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserRoleApiView(views.APIView):
    def get(self, request):
        data = {
            'roles': models.User.get_user_role_list()
        }
        return Response(data, status=status.HTTP_200_OK)


class GetUserStatusApiView(views.APIView):
    def get(self, request):
        data = {
            'status': models.User.get_user_status_list()
        }
        return Response(data, status=status.HTTP_200_OK)


class ProgrammerStatusApiView(views.APIView):
    def get(self, request):
        programmers = models.User.objects.filter(role=models.PROGRAMMER)
        serializer = serializers.ProgrammerSerializer(programmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
