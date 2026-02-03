
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("courses/", include("courses.urls")),
    path("accounts/", include("accounts.urls")),
]
