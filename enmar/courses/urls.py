from django.urls import path
from . import views

urlpatterns = [
    path("", views.category_list, name="category_list"),
    path("<int:category_id>/courses/", views.course_list, name="course_list"),
    path("", views.course_list, name="course_list"),
    path("<int:course_id>/", views.course_detail, name="course_detail"),
    path('enroll/<int:course_id>/', views.enroll, name='course_enroll'),
    path("lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
]
