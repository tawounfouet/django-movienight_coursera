from django.conf import settings
from django.test import TestCase

from movies.tasks import send_invitation, notify_of_starting_soon, send_attendance_change


class Question4TestCase(TestCase):
    def test_installed_apps_setup(self):
        self.assertIn("django_celery_results", settings.INSTALLED_APPS)

    def test_celery_settings(self):
        self.assertEqual(settings.CELERY_RESULT_BACKEND, "django-db")
        self.assertEqual(settings.CELERY_BROKER_URL, "redis://localhost:6379/0")

    def test_shared_task_decorator(self):
        # assume if shared_task is imported it's used as the decorator
        from movies.tasks import shared_task
        self.assertIsNotNone(shared_task)

    def test_functions_decorated(self):
        self.assertIsNotNone(send_invitation.delay)
        self.assertIsNotNone(send_attendance_change.delay)
        self.assertIsNotNone(notify_of_starting_soon.delay)
