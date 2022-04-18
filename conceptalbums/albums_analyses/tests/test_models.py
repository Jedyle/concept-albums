import pytest

from django.core.exceptions import ValidationError
from conceptalbums.utils import JSONSchemaValidator

from .factories import AlbumAnalysisFactory, LikeAnalysisFactory


@pytest.mark.django_db
class TestAlbumAnalysis:
    def test_str(self):
        analysis = AlbumAnalysisFactory()
        assert (
            str(analysis)
            == f"Analysis of {analysis.album} - by {analysis.user.username}"
        )

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
    def test_jsonschema_fail(self, analysis_json):
        analysis = AlbumAnalysisFactory(analysis=analysis_json)
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
                "tracks": {"1": {"analysis": "test"}, "3": {"analysis": "my analysis"}},
            },  # full
            {"tracks": {"1": {"analysis": "test"}}},  # only track analyses
        ],
    )
    def test_jsonschema_success(self, analysis_json):
        analysis = AlbumAnalysisFactory(analysis=analysis_json)
        analysis.full_clean()  # should return nothing as there is no error


@pytest.mark.django_db
class TestLikeAnalysis:

    def test_str(self):
        like = LikeAnalysisFactory()
        assert str(like) == f"User {like.user.username} likes '{like.analysis}'"
