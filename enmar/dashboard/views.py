# dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy("login"))
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def reports(request):
    return render(request, "dashboard/reports.html")

@login_required
def settings(request):
    return render(request, "dashboard/settings.html")
