from rest_framework import generics

from albums_analyses.models import AlbumAnalysis
from albums_analyses.api.serializers import (
    AlbumAnalysisListSerializer,
    AlbumAnalysisDetailsSerializer,
)

from albums_analyses.api.filters import AlbumAnalysisFilter


class AnalysisListView(generics.ListAPIView):
    def get_queryset(self):
        return AlbumAnalysis.objects.filter(album__slug=self.kwargs["slug"])

    serializer_class = AlbumAnalysisListSerializer
    filterset_class = AlbumAnalysisFilter


class AnalysisDetailsView(generics.RetrieveAPIView):

    queryset = AlbumAnalysis.objects.all()
    serializer_class = AlbumAnalysisDetailsSerializer
