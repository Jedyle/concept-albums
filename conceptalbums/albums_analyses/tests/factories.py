import factory
import factory.fuzzy

from authentication.tests.factories import UserFactory
from albums.tests.factories import AlbumFactory


class AlbumAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "albums_analyses.AlbumAnalysis"

    album = factory.SubFactory(AlbumFactory)
    user = factory.SubFactory(UserFactory)

    analysis = dict()


class LikeAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "albums_analyses.LikeAnalysis"

    analysis = factory.SubFactory(AlbumAnalysisFactory)
    user = factory.SubFactory(UserFactory)
