from django.db.models import Count
import django_filters as filters
from albums_analyses.models import AlbumAnalysis


class AlbumAnalysisFilter(filters.FilterSet):
    class Meta:
        model = AlbumAnalysis
        fields = {"user__username": ["exact", "icontains"]}


def filter_nb_likes(queryset, request):
    ordering = request.query_params.get("ordering")
    if ordering:
        params = ordering.split(",")
        if "nb_likes" in params:
            return queryset.annotate(nb_likes=Count("likes")).order_by("nb_likes")
        elif "-nb_likes" in params:
            return queryset.annotate(nb_likes=Count("likes")).order_by("-nb_likes")
    return queryset
