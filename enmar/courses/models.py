from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:category_detail", kwargs={"slug": self.slug})
    
# append to same file (or keep in same file block as above)
class Course(models.Model):
    category = models.ForeignKey(Category, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Optional maximum number of students")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("category", "slug")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"category_slug": self.category.slug, "course_slug": self.slug})

    def enrolled_count(self):
        return self.enrollments.count()

    def is_full(self):
        return self.capacity is not None and self.enrolled_count() >= self.capacity
    
# append Enrollment model
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} -> {self.course} ({self.status})"
    


class Activity(models.Model):
    ACTION_CHOICES = [
        ("course_created", "Course created"),
        ("course_updated", "Course updated"),
        ("course_deleted", "Course deleted"),
        ("enrolled", "User enrolled"),
        ("unenrolled", "User unenrolled"),
        ("admin_note", "Admin note"),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="activities")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    # optional link to course (nullable)
    course = models.ForeignKey("courses.Course", null=True, blank=True, on_delete=models.CASCADE, related_name="activities")
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    # Use models.JSONField (Django>=3.1). If on older Django and Postgres, switch import.
    try:
        from django.db.models import JSONField as _JSONField  # Django >= 3.1
    except Exception:
        from django.contrib.postgres.fields import JSONField as _JSONField  # fallback for older versions + Postgres
    metadata = _JSONField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        who = getattr(self.user, "username", "System")
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {who}: {self.get_action_display()}"

    @classmethod
    def log(cls, *, user=None, action, course=None, metadata=None):
        return cls.objects.create(user=user, action=action, course=course, metadata=metadata or {})