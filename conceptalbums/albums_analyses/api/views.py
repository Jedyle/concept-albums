from django.shortcuts import get_object_or_404
from rest_framework import generics, views, permissions, status
from rest_framework.response import Response

from albums.models import Album
from albums_analyses.models import AlbumAnalysis, LikeAnalysis
from albums_analyses.api.serializers import (
    AlbumAnalysisListSerializer,
    AlbumAnalysisDetailsSerializer,
    LikeAnalysisSerializer,
)

from albums_analyses.api.filters import AlbumAnalysisFilter


class AnalysisListView(generics.ListAPIView):
    def get_queryset(self):
        album = get_object_or_404(Album, slug=self.kwargs["slug"])
        return AlbumAnalysis.objects.filter(album=album)

    serializer_class = AlbumAnalysisListSerializer
    filterset_class = AlbumAnalysisFilter


class AnalysisDetailsView(generics.RetrieveAPIView):

    queryset = AlbumAnalysis.objects.all()
    serializer_class = AlbumAnalysisDetailsSerializer


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
