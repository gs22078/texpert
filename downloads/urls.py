from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'downloads'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:owner>/<str:repo>/', views.repo_page, name='repo_page'),
    path('<str:owner>/<str:repo>/d/<str:ref>/<path:path>/', views.download_repo, name='download_repo'),
    path('<str:owner>/<str:repo>/f/<str:ref>/<path:path>/', views.download_file, name='download_file'),
    path('<str:owner>/<str:repo>/o/<str:ref>/<path:path>.zip', views.open_in_overleaf_zip, name='open_in_overleaf_zip'),
    path('<str:owner>/<str:repo>/o/<str:ref>/<path:path>/', views.open_in_overleaf, name='open_in_overleaf'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)