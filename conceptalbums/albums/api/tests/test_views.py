import pytest

from rest_framework import status
from albums.tests.factories import AlbumFactory, ArtistFactory, TrackFactory
from faker import Faker


@pytest.mark.django_db
class TestListAlbums:

    URL = "/api/albums/"

    def test_list_albums(self, client):
        artist = ArtistFactory()
        album = AlbumFactory()
        album.artists.add(artist)
        album.save()
        # create tracks to be sure they're not displayed in results
        TrackFactory.create_batch(10, album=album)
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        res = response.json()
        assert res["count"] == 1
        assert res["next"] is None
        assert res["previous"] is None
        # ensure we dont display tracks in list
        for album in res["results"]:
            assert "tracks" not in album
            for key in [
                "mbid",
                "slug",
                "title",
                "release_date",
                "cover",
                "tags",
                "album_type",
                "artists",
            ]:
                assert key in album, key


@pytest.mark.django_db
class TestRetrieveAlbum:

    URL = "/api/albums/{}/"

    def test_retrieve_album_not_exists(self, client):
        slug = Faker().slug()
        print(slug)
        response = client.get(self.URL.format(slug))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_album_ok(self, client):
        artist = ArtistFactory()
        album = AlbumFactory()
        album.artists.add(artist)
        album.save()
        response = client.get(self.URL.format(album.slug))
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert "tracks" in results
        assert "artists" in results
