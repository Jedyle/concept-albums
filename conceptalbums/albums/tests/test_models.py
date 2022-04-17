import pytest

from ..models import Album, Artist, Track
from .factories import AlbumFactory, TrackFactory, ArtistFactory


@pytest.mark.django_db
class TestAlbum:
    def test_default(self):
        album = AlbumFactory()
        assert str(album) == album.title
        assert album.album_type == "LP"
        assert album.slug, album.slug


@pytest.mark.django_db
class TestArtist:
    def test_default(self):
        artist = ArtistFactory()
        assert str(artist) == artist.name
        assert artist.slug, artist.slug


@pytest.mark.django_db
class TestTrack:
    def test_default(self):
        album = AlbumFactory()
        track = TrackFactory(album=album)
        assert str(track) == f"{track.track_number}. {track.title} ({album.title})"
