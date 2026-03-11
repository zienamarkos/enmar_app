from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, View

from .models import Category, Course, Enrollment
from .forms import EnrollmentForm
from django.shortcuts import get_object_or_404, redirect
from .models import Course, Enrollment, Activity


class CategoryListView(ListView):
    model = Category
    template_name = "courses/category_list.html"
    context_object_name = "categories"

class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return Course.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        return ctx

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get("category_slug")
        course_slug = self.kwargs.get("course_slug")
        return get_object_or_404(Course, category__slug=category_slug, slug=course_slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = self.get_object()
        ctx["is_enrolled"] = self.request.user.is_authenticated and Enrollment.objects.filter(user=self.request.user, course=course, status="active").exists()
        ctx["enrolled_count"] = course.enrolled_count()
        return ctx

@login_required(login_url=reverse_lazy("login"))
def enroll_course(request, category_slug, course_slug):
    """
    Idempotent enroll endpoint:
    - Creates Enrollment if none exists.
    - If an Enrollment exists but is not active, reactivate it.
    - If two requests race, catch IntegrityError and re-fetch the Enrollment.
    """
    course = get_object_or_404(Course, category__slug=category_slug, slug=course_slug)
    if request.method != "POST":
        return redirect(course.get_absolute_url())

    next_url = request.POST.get("next") or reverse("dashboard:dashboard")

    try:
        # Atomic block to group the operations
        with transaction.atomic():
            enrollment, created = Enrollment.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={"status": "active"},
            )

            # If the enrollment already existed but was not active, reactivate it.
            if not created and enrollment.status != "active":
                enrollment.status = "active"
                enrollment.save(update_fields=["status"])

    except IntegrityError:
        # A race created a duplicate row at the same time; fetch the existing one.
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if enrollment:
            if enrollment.status != "active":
                enrollment.status = "active"
                enrollment.save(update_fields=["status"])
        else:
            # Unexpected: re-raise so we can see the error during debugging
            raise

    # Log activity but don't let logging break the user flow
    try:
        Activity.log(user=request.user, action="enrolled", course=course, metadata={})
    except Exception:
        # swallow errors from activity logging to avoid 500s from auxiliary failure
        pass

    messages.success(request, "You have been enrolled in the course.")
    return redirect(next_url)

@login_required(login_url=reverse_lazy("login"))
def unenroll_course(request, category_slug, course_slug):
    course = get_object_or_404(Course, category__slug=category_slug, slug=course_slug)
    enrollment = Enrollment.objects.filter(user=request.user, course=course, status="active").first()
    if not enrollment:
        messages.info(request, "You are not enrolled in this course.")
        next_url = request.POST.get("next") or course.get_absolute_url()
        return redirect(next_url)

    # mark cancelled (keeps history); or use enrollment.delete() to remove entirely
    enrollment.status = "cancelled"
    enrollment.save(update_fields=["status"])
    # optional: log activity
    try:
        Activity.log(user=request.user, action="unenrolled", course=course, metadata={"enrollment_id": enrollment.pk})
    except Exception:
        pass

    messages.success(request, "You have been unenrolled from the course.")
    next_url = request.POST.get("next") or reverse("dashboard:dashboard")
    return redirect(next_url)