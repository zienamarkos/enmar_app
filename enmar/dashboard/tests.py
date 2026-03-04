from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from courses.models import Category, Course, Enrollment

User = get_user_model()


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="password")
        self.cat1 = Category.objects.create(title="Science")
        self.course1 = Course.objects.create(category=self.cat1, title="Biology")
        self.course2 = Course.objects.create(category=self.cat1, title="Chemistry")
        # create an enrollment for the user
        Enrollment.objects.create(user=self.user, course=self.course1)

    def test_dashboard_shows_user_enrollments_and_courses(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")
        # enrolled course should be visible
        self.assertIn(self.course1.title, content)
        # other available courses should be visible
        self.assertIn(self.course2.title, content)
        # unenroll/enroll buttons are present (check for form action urls)
        enroll_action = reverse("courses:enroll", kwargs={"category_slug": self.course2.category.slug, "course_slug": self.course2.slug})
        unenroll_action = reverse("courses:unenroll", kwargs={"category_slug": self.course1.category.slug, "course_slug": self.course1.slug})
        self.assertIn(enroll_action, content)
        self.assertIn(unenroll_action, content)