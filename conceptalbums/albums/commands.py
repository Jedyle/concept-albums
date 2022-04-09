from django.db import transaction

from .models import Album, Track, Artist

from albums.scraper.parse_album import ParseAlbum
from albums.scraper.parse_lyrics import GeniusClient


@transaction.atomic
def create_album_from_musicbrainz_and_genius(mbid):
    """
    This function creates an album, the associated artists
    (if they don't already exist) the tracks of this albums with their lyrics.
    The data is fetched from musicbrainz (for album and artists)
    and genius (for lyrics)
    """
    album_parser = ParseAlbum(mbid)
    album_parser.load()
    album_data = album_parser.as_dict()

    print(album_data)

    artists_data = album_data.pop("artists", [])
    tracks_data = album_data.pop("tracks", [])

    print(f"Creating album {album_data['title']}")
    print(album_data)
    album = Album(**album_data)
    album.save()

    for artist_data in artists_data:
        artist, created = Artist.objects.get_or_create(**artist_data)
        if created:
            print(f"Created artist {artist_data['name']}")
        print(f"Linking album to artist {artist_data['name']}")
        album.artists.add(artist)
        artist.save()

    print("Fetching tracks...")
    genius_client = GeniusClient()
    for index, track in enumerate(tracks_data):
        lyrics = genius_client.get_song_lyrics(
            artists_data[0]["name"],
            track["title"]
        )
        print(f"Found lyrics for {track['title']}...")
        track = Track(
            title=track["title"], lyrics=lyrics, track_number=index+1
        )
        track.album = album
        track.save()
