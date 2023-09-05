from django.urls import path

from . import views

app_name = 'downloads'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:owner>/<str:repo>/', views.repo_page, name='repo_page'),
    path('<str:owner>/<str:repo>/d/<str:ref>/<path:path>/', views.download_repo, name='download_repo'),
    path('<str:owner>/<str:repo>/f/<str:ref>/<path:path>/', views.download_file, name='download_file'),
]