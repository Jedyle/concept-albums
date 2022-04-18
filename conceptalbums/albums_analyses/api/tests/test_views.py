import pytest
from faker import Faker
from rest_framework import status
from albums.tests.factories import AlbumFactory
from albums_analyses.tests.factories import AlbumAnalysisFactory


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
