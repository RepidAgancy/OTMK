from django.urls import path

from account.employee import views

urlpatterns = [
    path('my-problems/', views.MyProblemsApiView.as_view()),
    path('send-problem/', views.SendProblemApiView.as_view()),
    path('solved-problems/', views.GetSolvedProblemsApiView.as_view()),
    path('check-problem-is-solved/<int:problem_id>/', views.CheckProblemSolvedApiView.as_view()),
]