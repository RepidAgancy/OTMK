from django.urls import path, include

from account.leader.dashboard import views as dashboard_views
from account.leader.developers import views as developer_views
from account.leader.problems import views as problem_views
from account.leader.tasks import views as task_views

urlpatterns = [
    path(
        'dashboard/',
        include(
            [
                path('statistics/', dashboard_views.StatisticsApiView.as_view()),
                path('problems/statistics/', dashboard_views.AllProblemsApiView.as_view()),
                path('monthly-statistics/', dashboard_views.MonthlyStatisticsApiView.as_view()),
                path('problems/', dashboard_views.ProblemsApiView.as_view()),
            ]
        )
    ),
    path(
        'developers/',
        include(
            [
                path('developer/list/', developer_views.ProgrammersApiView.as_view()),
                path(
                    'developer/<int:developer_id>/problems/', developer_views.ProgrammerSolvedProblemsApiView.as_view(),
                ),
                path(
                  'developer/<int:developer_id>/calendar/', developer_views.DeveloperKeepBusiesApiView.as_view(),
                ),
                path(
                    'developer/add/', developer_views.DeveloperAddApiView.as_view(),
                )
            ]
        )
    ),
    path(
        'problems/',
        include(
            [
                path('problems/', problem_views.ProblemsApiView.as_view()),
            ]
        )
    ),
    path(
        'tasks/', include(
            [
                path('create/board/', task_views.CreateBoardApiView.as_view()),
                path(
                    'create/task/', task_views.CreateTaskApiView.as_view(),
                ),
                path(
                    'update/task/<int:id>/', task_views.UpdateTaskApiView.as_view(),
                ),
                path(
                    'get/task/<int:id>/', task_views.GetTaskApiView.as_view(),
                ),
                path(
                    'boards/', task_views.BoardApiView.as_view(),
                ),
                path(
                    'task-developers/', task_views.TaskDeveloperListApiView.as_view()
                ),
                path(
                    'delete/task/<int:id>/', task_views.DeleteTaskApiView.as_view(),
                ),
                path(
                    'delete/board/<int:id>/', task_views.DeleteBoardApiView.as_view()
                )
            ]
        )
    )
]