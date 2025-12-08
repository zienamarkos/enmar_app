from django.db import models
from accounts.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserCourseEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} → {self.course}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField()      # you can store markdown here
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} → {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
