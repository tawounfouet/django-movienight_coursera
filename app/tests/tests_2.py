from unittest import mock

from django.conf import settings
from django.test import TestCase

from movies.api.serializers import (
    MovieNightCreateSerializer,
    MovieNightSerializer,
    MovieSerializer,
)
from movies.api.views import MovieViewSet, MovieNightViewSet
from movies.models import Movie


class Question2TestCase(TestCase):
    def test_drf_settings(self):
        drf_settings = settings.REST_FRAMEWORK

        self.assertEqual(
            drf_settings["DEFAULT_PERMISSION_CLASSES"],
            ["rest_framework.permissions.IsAuthenticated"],
        )
        self.assertIn(
            "rest_framework.authentication.BasicAuthentication",
            drf_settings["DEFAULT_AUTHENTICATION_CLASSES"],
        )
        self.assertIn(
            "rest_framework.authentication.SessionAuthentication",
            drf_settings["DEFAULT_AUTHENTICATION_CLASSES"],
        )
        self.assertIn(
            "rest_framework.authentication.TokenAuthentication",
            drf_settings["DEFAULT_AUTHENTICATION_CLASSES"],
        )
        self.assertIn(
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            drf_settings["DEFAULT_AUTHENTICATION_CLASSES"],
        )
        self.assertEqual(
            drf_settings["DEFAULT_PAGINATION_CLASS"],
            "rest_framework.pagination.PageNumberPagination",
        )

    @staticmethod
    def test_movie_view_set_movie_fill():
        mvs = MovieViewSet()
        mvs.request = mock.MagicMock()
        mvs.kwargs = {"pk": 1}

        movie = mock.MagicMock()
        with mock.patch(
            "rest_framework.generics.get_object_or_404"
        ) as mock_get_object_or_404:
            mock_get_object_or_404.return_value = movie

            with mock.patch(
                "movies.api.views.fill_movie_details"
            ) as mock_fill_movie_details:
                mvs.get_object()
                mock_fill_movie_details.assert_called_with(movie)

    def test_movie_night_view_set_get_serializer_post(self):
        mnvs = MovieNightViewSet()
        mnvs.action = "create"
        post_request = mock.MagicMock()
        post_request.method = "POST"
        mnvs.request = post_request
        self.assertEqual(mnvs.get_serializer_class(), MovieNightCreateSerializer)

    def test_movie_night_view_set_get_serializer_non_post(self):
        mnvs = MovieNightViewSet()
        mnvs.action = "retrieve"
        get_request = mock.MagicMock()
        get_request.method = "GET"
        mnvs.request = get_request
        self.assertEqual(mnvs.get_serializer_class(), MovieNightSerializer)

    def test_movie_serializer(self):
        self.assertEqual(MovieSerializer.Meta.model, Movie)

        fields_set = {
            "title",
            "year",
            "runtime_minutes",
            "imdb_id",
            "genres",
            "plot",
            "is_full_record",
        }

        fields_all_str = MovieSerializer.Meta.fields == "__all__"
        fields_all_list = set(MovieSerializer.Meta.fields) == fields_set

        self.assertTrue(fields_all_str or fields_all_list)

        self.assertEqual(set(MovieSerializer.Meta.read_only_fields), fields_set)
