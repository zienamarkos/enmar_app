
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    # path("", views.CategoryListView.as_view(), name="category_list"),
    # path("category/<slug:slug>/", views.CourseListView.as_view(), name="category_detail"),
    # path("category/<slug:category_slug>/course/<slug:course_slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    # path("category/<slug:category_slug>/course/<slug:course_slug>/enroll/", views.enroll_course, name="enroll"),
    path("", views.CategoryListView.as_view(), name="course_category_list"),
    path("category/<slug:slug>/", views.CourseListView.as_view(), name="category_detail"),
    path("category/<slug:category_slug>/course/<slug:course_slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("category/<slug:category_slug>/course/<slug:course_slug>/enroll/", views.enroll_course, name="enroll"),

    path("category/<slug:category_slug>/course/<slug:course_slug>/unenroll/", views.unenroll_course, name="unenroll"),
]
