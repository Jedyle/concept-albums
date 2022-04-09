import pytest

from ..models import Album, Artist, Track

@pytest.mark.django_db
class TestAlbum:

    def test_default(self):
        album = Album.objects.create(
            title = "Test"
        )
        assert str(album) == album.title
        assert album.album_type == "LP"


@pytest.mark.django_db
class TestArtist:

    def test_default(self):
        artist = Artist.objects.create(
            name = "Test"
        )
        assert str(artist) == artist.name


@pytest.mark.django_db
class TestTrack:

    def test_default(self):
        album = Album.objects.create(
            title = "Test"
        )
        track = Track.objects.create(
            album = album,
            track_number = 1,
            name = "MyTrack",
            lyrics = "Some\nLyrics"
        )
        assert str(track) == f"{track.track_number}. {track.name} ({album.title})"
