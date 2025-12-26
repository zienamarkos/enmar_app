from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.dashboard_home, name="dashboard_home"),
]
