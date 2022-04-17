from rest_framework import generics

from albums.models import Album
from albums.api.serializers import AlbumListSerializer, AlbumDetailsSerializer
from albums.api.filters import AlbumFilter


class AlbumList(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumListSerializer
    filterset_class = AlbumFilter


class AlbumRetrieve(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailsSerializer
    lookup_field = "slug"
