from rest_framework import serializers

from albums.models import Album, Track, Artist


class _NestedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["title", "track_number", "lyrics"]


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["name", "slug", "mbid"]


class AlbumDetailsSerializer(serializers.ModelSerializer):

    tracks = _NestedTrackSerializer(many=True, read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = "__all__"


class AlbumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            "mbid",
            "slug",
            "title",
            "release_date",
            "cover",
            "tags",
            "album_type",
            "artists"
        ]
    artists = ArtistSerializer(many=True, read_only=True)
        
