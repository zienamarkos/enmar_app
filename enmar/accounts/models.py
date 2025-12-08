
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("instructor", "Instructor"),
        ("analyst", "SOC Analyst"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    level = models.IntegerField(default=1)
    badges = models.TextField(blank=True, null=True)  # store JSON or CSV list

    def __str__(self):
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
