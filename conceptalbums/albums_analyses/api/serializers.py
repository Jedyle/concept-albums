from rest_framework import serializers

from albums.models import Album
from albums.api.serializers import AlbumDetailsSerializer
from albums_analyses.models import AlbumAnalysis, LikeAnalysis


class AlbumAnalysisListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumAnalysis
        fields = ["id", "album", "user", "analysis", "likes"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    album = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()


class AlbumAnalysisDetailsSerializer(serializers.ModelSerializer):
    """
    Gets a full analysis and the complete lyrics of the album
    This way it's easy to add some comparison feature in the frontend
    """

    class Meta:
        model = AlbumAnalysis
        fields = ["id", "album", "user", "analysis", "likes", "logged_user_like"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    album = AlbumDetailsSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    logged_user_like = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_logged_user_like(self, obj):
        if "request" in self.context and self.context["request"].user.is_authenticated:
            return LikeAnalysis.objects.filter(
                analysis=obj, user=self.context["request"].user
            ).exists()


class AlbumAnalysisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumAnalysis
        fields = ["album", "analysis"]

    album = serializers.SlugRelatedField(
        slug_field="slug", queryset=Album.objects.all()
    )


class LikeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeAnalysis
        fields = ["user", "analysis", "created_at", "updated_at"]

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    analysis = serializers.PrimaryKeyRelatedField(read_only=True)
