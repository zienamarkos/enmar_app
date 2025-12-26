from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Category, Enrollment
from django.contrib.auth.decorators import login_required

def category_list(request):
    categories = Category.objects.all()
    return render(request, "courses/category_list.html", {
        "categories": categories
    })

def course_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = category.courses.all()
    return render(request, "courses/course_list.html", {
        "category": category,
        "courses": courses
    })



def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect('course_detail', course_id=course.id)

