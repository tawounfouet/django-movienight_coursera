import re

from crispy_forms.layout import Submit
from django.conf import settings
from django.core import mail
from django.test import TestCase
from django_registration.forms import RegistrationForm as DefaultRegistrationForm

from movienight_auth.forms import RegistrationForm
from movienight_auth.models import User


class Question3TestCase(TestCase):
    def test_crispy_settings(self):
        self.assertIn("crispy_forms", settings.INSTALLED_APPS)
        self.assertIn("crispy_bootstrap5", settings.INSTALLED_APPS)
        self.assertEqual(settings.CRISPY_ALLOWED_TEMPLATE_PACKS, "bootstrap5")
        self.assertEqual(settings.CRISPY_TEMPLATE_PACK, "bootstrap5")

    def _try_login(self):
        return self.client.post(
            "/accounts/login/",
            {"username": "user@example.com", "password": "MyGreatWord!@#"},
        )

    def test_registration_form(self):
        self.assertEqual(RegistrationForm.Meta.model, User)
        self.assertTrue(issubclass(RegistrationForm, DefaultRegistrationForm))
        reg_form = RegistrationForm()
        self.assertIsInstance(reg_form.helper.inputs[0], Submit)

    def test_registration_flow(self):
        reg_response = self.client.post(
            "/accounts/register/",
            {
                "email": "user@example.com",
                "password1": "MyGreatWord!@#",
                "password2": "MyGreatWord!@#",
            },
        )
        self.assertEqual(reg_response.status_code, 302)
        self.assertEqual(
            reg_response.headers["Location"], "/accounts/register/complete/"
        )
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertIn(
            "You registered for Movie Night, but you need to activate your account within 7 days.",
            message.body,
        )
        confirm_link_res = re.search(r"(https?://testserver/[^\s]+)", message.body)
        confirm_link = confirm_link_res.group(1)

        fail_login_response = self._try_login()

        self.assertIn(
            b"Please enter a correct email address and password",
            fail_login_response.content,
        )

        confirm_resp = self.client.get(confirm_link)
        self.assertEqual(confirm_resp.status_code, 302)
        self.assertEqual(
            confirm_resp.headers["Location"], "/accounts/activate/complete/"
        )

        success_login_response = self._try_login()

        self.assertEqual(success_login_response.status_code, 302)
        self.assertEqual(
            success_login_response.headers["Location"], "/accounts/profile/"
        )
