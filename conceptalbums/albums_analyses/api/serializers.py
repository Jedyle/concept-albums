from rest_framework import serializers

from albums_analyses.models import AlbumAnalysis


class AlbumAnalysisListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumAnalysis
        fields = ["id", "album", "user", "analysis"]

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    album = serializers.SlugRelatedField(slug_field="slug", read_only=True)
