from django.urls import path, include

from account.developer.problems import views as problem_views
from account.developer.tasks import views as task_views
from account.developer.profile import views as profile_views

urlpatterns = [
    path('problems/', include(
        [
            path('problems/', problem_views.ProblemListApiView.as_view()),
            path("start/problem-solve/<int:problem_id>/", problem_views.SolveProblemApiView.as_view()),
            path("end/problem-solve/<int:problem_id>/", problem_views.ProblemIsSolvedApiView.as_view()),
            path("keep/busy/programmer/", problem_views.KeepBusyApiView.as_view()),
            path("keep/not-busy/programmer/", problem_views.UserKeepNotBusyApiView.as_view()),
        ]
    )),
    path('tasks/', include(
        [
            path('tasks/', task_views.TasksApiView.as_view()),
            path('tasks/<int:id>/update/', task_views.UpdateTaskApiView.as_view()),
        ]
    )),
    path('profile/', include(
         [
            path('solved_problems/', profile_views.SolvedProblemsApiView.as_view()),
            path('calendar/', profile_views.ProfileKeepBusyApiView.as_view()),
            path('profile/', profile_views.ProfileApiView.as_view()),
            path('profile/change/', profile_views.ProfileChangeApiView.as_view()),
        ]
    )),

]