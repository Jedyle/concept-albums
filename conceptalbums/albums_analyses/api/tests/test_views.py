import pytest
from faker import Faker
from rest_framework import status
from albums.tests.factories import AlbumFactory
from albums_analyses.models import LikeAnalysis, AlbumAnalysis
from albums_analyses.tests.factories import AlbumAnalysisFactory, LikeAnalysisFactory


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="user", password="password")


@pytest.fixture
def logged_client(user, client):
    client.force_login(user)
    return client


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

    def test_ordering(self, client):
        """
        Test ordering by nb of likes
        """
        album = AlbumFactory()
        analyses = AlbumAnalysisFactory.create_batch(5, album=album)

        LikeAnalysisFactory.create_batch(2, analysis=analyses[0])
        LikeAnalysisFactory.create_batch(1, analysis=analyses[1])
        LikeAnalysisFactory.create_batch(5, analysis=analyses[2])
        LikeAnalysisFactory.create_batch(3, analysis=analyses[3])

        ### 1. Reverse order

        response = client.get(self.URL.format(album.slug) + "?ordering=-nb_likes")

        # results should be sorted by reverse number of likes, so
        # 2, 3, 0, 1, 4

        results = response.json()["results"]
        assert results[0]["id"] == analyses[2].id
        assert results[1]["id"] == analyses[3].id
        assert results[2]["id"] == analyses[0].id
        assert results[3]["id"] == analyses[1].id
        assert results[4]["id"] == analyses[4].id

        ### 2. Ascending order

        response = client.get(self.URL.format(album.slug) + "?ordering=nb_likes")

        # results should be sorted by number of likes, so
        # 4, 1, 0, 3, 2

        results = response.json()["results"]
        assert results[0]["id"] == analyses[4].id
        assert results[1]["id"] == analyses[1].id
        assert results[2]["id"] == analyses[0].id
        assert results[3]["id"] == analyses[3].id
        assert results[4]["id"] == analyses[2].id


@pytest.mark.django_db
class TestAnalysisCreate:

    URL = "/api/albums_analyses/"

    def test_anonymous(self, client):
        album = AlbumFactory()
        response = client.post(
            self.URL,
            {"album": album.slug, "analysis": {"global": "example"}},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_ok(self, user, logged_client):
        album = AlbumFactory()
        response = logged_client.post(
            self.URL,
            {"album": album.slug, "analysis": {"global": "example"}},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert AlbumAnalysis.objects.filter(user=user, album=album).exists()

    def test_wrong_album_slug(self, user, logged_client):
        response = logged_client.post(
            self.URL,
            {"album": "fake-slug", "analysis": {"global": "example"}},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

    def test_already_exists(self, user, logged_client):
        album = AlbumFactory()
        AlbumAnalysisFactory(user=user, album=album)
        response = logged_client.post(
            self.URL,
            {"album": album.slug, "analysis": {"global": "example"}},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAnalysisDetailsView:

    URL = "/api/albums_analyses/{}/"

    def test_not_found(self, client):
        id_ = Faker().random_int()
        response = client.get(self.URL.format(id_))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ok(self, client):
        analysis = AlbumAnalysisFactory()
        response = client.get(self.URL.format(analysis.pk))
        assert response.status_code == status.HTTP_200_OK

        # make sure there is all album data in json
        res_json = response.json()
        assert res_json["logged_user_like"] is None
        album = res_json["album"]
        assert "tracks" in album

    def test_logged_user_sees_likes(self, user, logged_client):
        """
        If route is called by a logged user, there is an additiona info
        With whether the user likes the analysis (here true)
        """
        analysis = AlbumAnalysisFactory()
        like = LikeAnalysisFactory(analysis=analysis, user=user)
        response = logged_client.get(self.URL.format(analysis.pk))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["logged_user_like"] is True

    def test_logged_user_sees_not_like(self, user, logged_client):
        """
        If route is called by a logged user, there is an additiona info
        With whether the user likes the analysis (here false)
        """
        analysis = AlbumAnalysisFactory()
        response = logged_client.get(self.URL.format(analysis.pk))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["logged_user_like"] is False


@pytest.mark.django_db
class TestLikeAnalysisView:

    URL = "/api/albums_analyses/{}/like/"

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
