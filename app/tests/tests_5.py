from django.conf import settings
from django.test import TestCase
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from movies.schedule_setup import schedule_setup


class Question5TestCase(TestCase):
    def test_installed_apps_setup(self):
        self.assertIn("django_celery_beat", settings.INSTALLED_APPS)

    def test_schedule_setup(self):
        schedule_setup()
        interval_schedule = IntervalSchedule.objects.filter(
            every=1, period=IntervalSchedule.MINUTES
        ).first()

        self.assertIsNotNone(interval_schedule)

        period_tasks = PeriodicTask.objects.filter(interval=interval_schedule)

        self.assertEqual(len(period_tasks), 1)

        self.assertEqual(period_tasks[0].task, "movies.tasks.notify_of_starting_soon")
