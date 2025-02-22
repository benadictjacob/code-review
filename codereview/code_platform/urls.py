from django.urls import path
from . import views

urlpatterns = [
    path("", views.display, name="display"),
    path("upload/", views.upload_code, name="upload"),
    path("display_code/", views.display_code, name="display_code"),
]