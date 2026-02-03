from django.shortcuts import render, get_object_or_404
from .models import Category, Course
from django.contrib.auth.decorators import login_required

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "courses/category_list.html", {
        "categories": categories
    })

@login_required
def course_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, "courses/course_list.html", {
        "category": category,
        "courses": courses
    })

@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "courses/course_detail.html", {
        "course": course
    })
