from django.shortcuts import get_object_or_404
from rest_framework import generics, views, permissions, status, exceptions
from rest_framework.response import Response

from albums.models import Album
from albums_analyses.models import AlbumAnalysis, LikeAnalysis
from albums_analyses.api.serializers import (
    AlbumAnalysisListSerializer,
    AlbumAnalysisDetailsSerializer,
    AlbumAnalysisCreateSerializer,
    AlbumAnalysisUpdateSerializer,
    LikeAnalysisSerializer,
)

from albums_analyses.api.filters import AlbumAnalysisFilter, filter_nb_likes


class AnalysisListView(generics.ListAPIView):
    def get_queryset(self):
        album = get_object_or_404(Album, slug=self.kwargs["slug"])
        queryset = AlbumAnalysis.objects.filter(album=album)
        return filter_nb_likes(queryset, self.request)

    serializer_class = AlbumAnalysisListSerializer
    filterset_class = AlbumAnalysisFilter


class AnalysisDetailsView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == "GET":
            return AlbumAnalysis.objects.all()
        elif self.request.method in ("PUT", "PATCH"):
            return AlbumAnalysis.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AlbumAnalysisDetailsSerializer
        elif self.request.method in ("PUT", "PATCH"):
            return AlbumAnalysisUpdateSerializer


class AnalysisCreateView(generics.CreateAPIView):
    queryset = AlbumAnalysis.objects.all()
    serializer_class = AlbumAnalysisCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        album = serializer.validated_data["album"]
        if AlbumAnalysis.objects.filter(album=album, user=self.request.user).exists():
            raise exceptions.ValidationError("Analysis for this album already exists.")
        serializer.save(user=self.request.user)


class LikeAnalysisView(views.APIView):

    """
    POST /albums_analyses/id/like will create a like (or do nothing if already exists)
    DELETE /albums_analyses/id/like will delete the like
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, analysis_id):
        analysis = get_object_or_404(AlbumAnalysis, pk=analysis_id)
        user_like, created = LikeAnalysis.objects.get_or_create(
            user=request.user, analysis=analysis
        )
        response = LikeAnalysisSerializer(user_like).data
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, analysis_id):
        analysis = get_object_or_404(AlbumAnalysis, pk=analysis_id)
        user_like = get_object_or_404(
            LikeAnalysis, user=request.user, analysis=analysis
        )
        user_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
