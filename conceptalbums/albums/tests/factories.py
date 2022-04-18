import uuid
import factory
import factory.fuzzy


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "albums.Track"

    title = factory.fuzzy.FuzzyText(length=30)
    lyrics = factory.fuzzy.FuzzyText(length=300)
    track_number = factory.Sequence(lambda n: n)


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "albums.Artist"

    mbid = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Faker("name")


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "albums.Album"

    album_type = "LP"
    title = factory.fuzzy.FuzzyText(length=20)
    mbid = factory.LazyFunction(lambda: str(uuid.uuid4()))
