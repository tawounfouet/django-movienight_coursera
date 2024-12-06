from crispy_forms.layout import Submit
from django.test import TestCase

from movies.forms import MovieNightForm, InviteeForm, AttendanceForm


class Question4TestCase(TestCase):
    def test_movie_night_form(self):
        mnf = MovieNightForm()
        self.assertIsInstance(mnf.helper.inputs[0], Submit)
        self.assertEqual(mnf.helper.inputs[0].name, "submit")
        self.assertEqual(mnf.helper.inputs[0].value, "Create")

    def test_invitee_form(self):
        invitee_form = InviteeForm()
        self.assertIsInstance(invitee_form.helper.inputs[0], Submit)
        self.assertEqual(invitee_form.helper.inputs[0].name, "submit")
        self.assertEqual(invitee_form.helper.inputs[0].value, "Invite")

    def test_attendance_form(self):
        af = AttendanceForm()
        self.assertIsInstance(af.helper.inputs[0], Submit)
        self.assertEqual(af.helper.inputs[0].name, "submit")
        self.assertEqual(af.helper.inputs[0].value, "Update Attendance")
