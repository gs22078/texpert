from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:owner>/<str:repo>/', views.repo_page, name='repo_page'),
]