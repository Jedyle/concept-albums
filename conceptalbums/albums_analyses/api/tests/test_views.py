import pytest
from faker import Faker
from rest_framework import status
from albums.tests.factories import AlbumFactory
from albums_analyses.models import LikeAnalysis
from albums_analyses.tests.factories import AlbumAnalysisFactory, LikeAnalysisFactory


@pytest.mark.django_db
class TestAnalysisListView:

    URL = "/api/albums/{}/analyses/"

    def test_album_not_found(self, client):
        slug = Faker().slug()
        response = client.get(self.URL.format(slug))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ok(self, client):
        album = AlbumFactory()
        analyses = AlbumAnalysisFactory.create_batch(5, album=album)
        # these analyses should not be fetched in the results
        AlbumAnalysisFactory.create_batch(5)
        response = client.get(self.URL.format(album.slug))
        assert response.status_code == status.HTTP_200_OK
        res = response.json()
        assert res["count"] == 5, res["count"]
        for res_analysis in res["results"]:
            assert res_analysis["album"] == album.slug
            assert res_analysis["id"] in [a.pk for a in analyses]


@pytest.mark.django_db
class TestAnalysisDetailsView:

    URL = "/api/albums_analyses/{}"

    def test_not_found(self, client):
        id_ = Faker().random_int()
        response = client.get(self.URL.format(id_))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ok(self, client):
        analysis = AlbumAnalysisFactory()
        response = client.get(self.URL.format(analysis.pk))
        assert response.status_code == status.HTTP_200_OK

        # make sure there is all album data in json
        album = response.json()["album"]
        assert "tracks" in album


@pytest.mark.django_db
class TestLikeAnalysisView:

    URL = "/api/albums_analyses/{}/like"

    @pytest.fixture
    @staticmethod
    def user(django_user_model):
        return django_user_model.objects.create_user(
            username="user", password="password"
        )

    @pytest.fixture
    @staticmethod
    def logged_client(user, client):
        client.force_login(user)
        return client

    @pytest.fixture
    @staticmethod
    def analysis():
        return AlbumAnalysisFactory()

    def test_like_not_allowed_anonymous(self, client, analysis):
        response = client.post(self.URL.format(analysis.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_remove_not_allowed_anonymous(self, client, analysis):
        response = client.delete(self.URL.format(analysis.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_like_not_found(self, logged_client):
        fake_id = Faker().random_int()
        response = logged_client.post(self.URL.format(fake_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_remove_like_not_found(self, logged_client):
        fake_id = Faker().random_int()
        response = logged_client.delete(self.URL.format(fake_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_like_ok(self, logged_client, user, analysis):
        response = logged_client.post(self.URL.format(analysis.id))
        assert response.status_code == status.HTTP_201_CREATED
        assert LikeAnalysis.objects.get(user=user, analysis=analysis)

    def test_remove_like_ok(self, logged_client, user, analysis):
        LikeAnalysisFactory(analysis=analysis, user=user)
        response = logged_client.delete(self.URL.format(analysis.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(LikeAnalysis.DoesNotExist):
            LikeAnalysis.objects.get(user=user, analysis=analysis)
