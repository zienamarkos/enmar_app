
from django.urls import path
from . import views

urlpatterns = [
    path("", views.category_list, name="course_category_list"),
    path("<slug:slug>/", views.course_list, name="course_list"),
    path("course/<int:id>/", views.course_detail, name="course_detail"),
]

