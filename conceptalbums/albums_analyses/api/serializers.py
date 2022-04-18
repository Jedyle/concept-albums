from rest_framework import serializers

from albums.api.serializers import AlbumDetailsSerializer
from albums_analyses.models import AlbumAnalysis, LikeAnalysis


class AlbumAnalysisListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumAnalysis
        fields = ["id", "album", "user", "analysis"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    album = serializers.SlugRelatedField(slug_field="slug", read_only=True)


class AlbumAnalysisDetailsSerializer(serializers.ModelSerializer):
    """
    Gets a full analysis and the complete lyrics of the album
    This way it's easy to add some comparison feature in the frontend
    """

    class Meta:
        model = AlbumAnalysis
        fields = ["id", "album", "user", "analysis"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    album = AlbumDetailsSerializer(read_only=True)


class LikeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeAnalysis
        fields = ["user", "analysis", "created_at", "updated_at"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    analysis = serializers.PrimaryKeyRelatedField(read_only=True)
