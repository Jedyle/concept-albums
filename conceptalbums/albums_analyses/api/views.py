from django.shortcuts import get_object_or_404
from rest_framework import generics

from albums.models import Album
from albums_analyses.models import AlbumAnalysis
from albums_analyses.api.serializers import (
    AlbumAnalysisListSerializer,
    AlbumAnalysisDetailsSerializer,
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
