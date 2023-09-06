from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)