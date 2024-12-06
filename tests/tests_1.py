from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from django.test import TestCase

from movienight_auth.models import User, MovieNightUserManager


class Question1TestCase(TestCase):
    def test_auth_user_setting(self):
        self.assertEqual(settings.AUTH_USER_MODEL, "movienight_auth.User")

    def test_sub_class(self):
        self.assertTrue(issubclass(User, AbstractUser))

    def test_user_attributes(self):
        self.assertIsNone(User.username)
        self.assertIsInstance(User.email.field, models.EmailField)
        self.assertIsInstance(User.objects, MovieNightUserManager)
        self.assertEqual(User.USERNAME_FIELD, "email")
        self.assertEqual(User.REQUIRED_FIELDS, [])

    def test_email_unique_constraint(self):
        User.objects.create(email="user@example.com")
        with self.assertRaises(IntegrityError):
            User.objects.create(email="user@example.com")
