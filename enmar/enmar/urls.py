
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("courses/", include("courses.urls")),
    path("accounts/", include("accounts.urls")),
]

# Only enable browser-reload endpoints in DEBUG mode
if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]