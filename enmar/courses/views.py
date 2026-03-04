from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
    course = get_object_or_404(Course, category__slug=category_slug, slug=course_slug)

    # Prevent enroll if already enrolled
    existing = Enrollment.objects.filter(user=request.user, course=course, status="active").first()
    if existing:
        messages.info(request, "You are already registered for this course.")
        return redirect(course.get_absolute_url())

    # Optional capacity check
    if course.is_full():
        messages.error(request, "This course is full and cannot accept more registrations.")
        return redirect(course.get_absolute_url())

    if request.method == "POST":
        # create enrollment
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, "You have been registered for the course.")
        # Redirect to course page or dashboard; next param can be used if present
        next_url = request.POST.get("next") or reverse("courses:course_detail", kwargs={"category_slug": category_slug, "course_slug": course_slug})
        return redirect(next_url)

    # For GET, show a confirmation page if desired, or redirect to course page
    return render(request, "courses/enroll_confirm.html", {"course": course})

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