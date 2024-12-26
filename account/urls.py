from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account import views

urlpatterns = [
    path('user/login/', views.LoginApiView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/logout/', views.LogOutView.as_view(), name='logout'),
    path('user/profile/', views.UserProfileApiView.as_view(), name='profile'),
    path('user/roles/', views.GetUserRoleApiView.as_view(), name='user-roles'),
    path('user/status/', views.GetUserStatusApiView.as_view(), name='user-status'),
    path('programmer-status-list', views.ProgrammerStatusApiView.as_view(), name='programmer-status'),
]
