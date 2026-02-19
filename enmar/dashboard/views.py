# dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

@login_required
def reports(request):
    return render(request, "dashboard/reports.html")

@login_required
def settings(request):
    return render(request, "dashboard/settings.html")

# =====================================================================

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from courses.models import Category, Enrollment

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # All categories with prefetched courses for display
        ctx["categories"] = Category.objects.prefetch_related("courses").all()
        # Current user's active enrollments
        ctx["my_enrollments"] = (
            Enrollment.objects.filter(user=self.request.user, status="active")
            .select_related("course", "course__category")
        )
        ctx["enrolled_course_ids"] = {e.course_id for e in ctx["my_enrollments"]}
        return ctx