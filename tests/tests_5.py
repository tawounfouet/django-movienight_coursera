from unittest import mock

from django.db.models.signals import post_save, pre_save
from django.test import TestCase
from django.utils import timezone

from movienight_auth.models import User
from movies.models import Movie, MovieNight, MovieNightInvitation
from django.core import mail

from movies.signals import invitation_update, invitation_create


class Question5TestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            year=2001,
            runtime_minutes=60,
            imdb_id="fake_id",
            plot="A fake movie to test things.",
            is_full_record=True,
        )

        self.user1 = User.objects.create_user(email="user1@example.com", password="abc123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="abc123")

        self.movie_night = MovieNight.objects.create(
            movie=self.movie,
            creator=self.user1,
            start_time=timezone.now()
        )

        self.invitation = MovieNightInvitation.objects.create(
            movie_night=self.movie_night,
            invitee=self.user2
        )

    def test_invitation_create_signal(self):
        # invite should be there from the setUp
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertIn(self.user2.email, message.to)
        self.assertEqual("Invitation to watch Test Movie", message.subject)
        self.assertIn("user1@example.com has invited you", message.body)

    def test_invitation_response_signal(self):
        mail.outbox = []

        self.invitation.is_attending = True
        self.invitation.save()

        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertIn(self.user1.email, message.to)
        self.assertEqual("user2@example.com has update their attendance to your Movie Night", message.subject)
        self.assertIn("will be attending", message.body)

        # status hasn't changed so no email
        self.invitation.is_attending = True
        self.invitation.save(force_update=True)

        self.assertEqual(len(mail.outbox), 1)

        self.invitation.is_attending = False
        self.invitation.save()

        self.assertEqual(len(mail.outbox), 2)

        message = mail.outbox[1]

        self.assertIn(self.user1.email, message.to)
        self.assertEqual("user2@example.com has update their attendance to your Movie Night", message.subject)
        self.assertIn("will not be attending", message.body)

    def test_signal_setup(self):
        pre_save_listeners = pre_save._live_receivers(MovieNightInvitation)
        self.assertIn(invitation_update, pre_save_listeners)

        post_save_listeners = post_save._live_receivers(MovieNightInvitation)
        self.assertIn(invitation_create, post_save_listeners)
