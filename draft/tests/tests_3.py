from django.test import TestCase
from rest_framework.permissions import IsAuthenticated

from movies.api.permissions import IsCreatorPermission, IsInviteePermission
from movies.api.views import MovieNightViewSet, MovieNightInvitationViewSet


class Question3TestCase(TestCase):
    def test_is_creator_definition(self):
        self.assertEqual(IsCreatorPermission.user_field, "creator")

    def test_is_invitee_definition(self):
        self.assertEqual(IsInviteePermission.user_field, "invitee")

    def test_movie_night_view_set_permission_classes(self):
        op_classes = {
            MovieNightViewSet.permission_classes[0].op1_class,
            MovieNightViewSet.permission_classes[0].op2_class,
        }
        self.assertEqual(op_classes, {IsAuthenticated, IsCreatorPermission})

    def test_movie_night_invitation_view_set_permission_classes(self):
        op_classes = {
            MovieNightInvitationViewSet.permission_classes[0].op1_class,
            MovieNightInvitationViewSet.permission_classes[0].op2_class,
        }
        self.assertEqual(op_classes, {IsAuthenticated, IsInviteePermission})
