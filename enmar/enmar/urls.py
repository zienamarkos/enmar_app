
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("", include("courses.urls")), # Set courses as the homepage
    path("accounts/", include("dashboard.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
