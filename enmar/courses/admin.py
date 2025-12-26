
from django.contrib import admin
from .models import Category, Course, Enrollment

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CourseInline]

admin.site.register(Course)
admin.site.register(Enrollment)

