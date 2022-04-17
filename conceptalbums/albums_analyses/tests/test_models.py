import pytest
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from conceptalbums.utils import JSONSchemaValidator
from albums.models import Album
from albums_analyses.models import AlbumAnalysis


@pytest.mark.django_db
class TestAlbumAnalysis:
    @pytest.fixture
    @staticmethod
    def album_and_user():
        album = Album.objects.create(title="Test")
        user = User.objects.create(username="testuser", password="testpass")
        return album, user

    def test_str(self, album_and_user):
        album, user = album_and_user
        analysis = AlbumAnalysis.objects.create(album=album, user=user, analysis={})
        assert str(analysis) == f"Analysis of {album} - by {user.username}"

    @pytest.mark.parametrize(
        "analysis_json",
        [
            {"lol": "mdr"},  # additionalProperty not allowed
            {"global": 10},  # should be string
            {"global": "test", "lol": "mdr"},  # additionalProperty
            {"tracks": {"wrong": "string"}},  # wrong pattern inside 'tracks'
            {"tracks": {"1": "test"}},  # must be dict nested in each track nb
            {"tracks": {"1": {"analysis": 1}}},  # analysis must be string
        ],
    )
    def test_jsonschema_fail(self, album_and_user, analysis_json):
        album, user = album_and_user
        analysis = AlbumAnalysis(album=album, user=user, analysis=analysis_json)
        with pytest.raises(ValidationError) as e:
            analysis.full_clean()
        assert (
            JSONSchemaValidator.ERROR_MESSAGE.format(analysis_json)
            in e.value.message_dict["analysis"]
        )

    @pytest.mark.parametrize(
        "analysis_json",
        [
            {"global": "test"},  # only global analysis
            {
                "global": "test",
                "tracks": {
                    "1": {"analysis": "test"},
                    "3": {"analysis": "my analysis"}
                },
            },  # full
            {"tracks": {"1": {"analysis": "test"}}},  # only track analyses
        ],
    )
    def test_jsonschema_success(self, album_and_user, analysis_json):
        album, user = album_and_user
        analysis = AlbumAnalysis(album=album, user=user, analysis=analysis_json)
        analysis.full_clean()  # should return nothing as there is no error
