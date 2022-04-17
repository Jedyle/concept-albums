import django_filters as filters
from albums.models import Album


class AlbumFilter(filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "title": ["exact", "icontains"],
            "slug": ["exact"],
            "release_date": ["exact", "year__gt", "year__lt"],
            "album_type": ["exact"]
        }
