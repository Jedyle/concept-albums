import django_filters as filters
from albums_analyses.models import AlbumAnalysis


class AlbumAnalysisFilter(filters.FilterSet):
    class Meta:
        model = AlbumAnalysis
        fields = {
            "user__username": ["exact", "icontains"]
        }
