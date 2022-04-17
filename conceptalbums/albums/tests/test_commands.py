import pytest

from albums.models import Album, Track
from albums.commands import create_album_from_musicbrainz_and_genius


@pytest.mark.api
@pytest.mark.django_db
def test_create_album_from_musicbrainz_and_genius():
    # Vektor - Terminal Redux
    mbid = "8c14bbdd-de87-48fa-8cc9-153c3d56583e"
    create_album_from_musicbrainz_and_genius(mbid)
    album = Album.objects.get(mbid=mbid)
    assert album
    assert album.artists
    assert Track.objects.filter(album=album).count() == 10
