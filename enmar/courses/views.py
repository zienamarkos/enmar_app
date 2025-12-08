from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Lesson, Category, UserCourseEnrollment
from django.contrib.auth.decorators import login_required

def category_list(request):
    categories = Category.objects.all()
    return render(request, "courses/category_list.html", {"categories": categories})


def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = category.courses.all()
    return render(request, "courses/courses_by_category.html", {
        "category": category,
        "courses": courses
    })



def course_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = category.courses.all()
    return render(request, "courses/course_list.html", {"category": category, "courses": courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, "courses/lesson_detail.html", {"lesson": lesson})


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourseEnrollment.objects.get_or_create(user=request.user, course=course)
    return redirect("course_detail", course_id=course.id)
