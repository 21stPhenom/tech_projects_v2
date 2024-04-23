from django.urls import path
from projects import views

app_name = 'projects'
urlpatterns = [
    path('', views.projects, name='projects'),
    path('create/', views.create_project, name='create-project'),
    path('solutions/', views.solutions, name='solutions'),
    path('<str:project_slug>/', views.project_detail, name='project-detail'),
    path('<str:project_slug>/enroll/', views.enroll, name='enroll'),
    path('<str:project_slug>/update/', views.update_project, name='update-project'),
    path('<str:project_slug>/delete/', views.delete_project, name='delete_project'),

    path('<str:project_slug>/solutions/create', views.create_solution, name='create-solution'),
    path('solutions/<str:uid>/', views.solution_detail, name='solution-detail'),
    path('solutions/<str:uid>/delete/', views.delete_solution, name='delete-solution'),
    path('solutions/<str:uid>/update/', views.update_solution, name='update-solution'),
]