from django.db import models
from conceptalbums.utils import unique_slug_generator


class Album(models.Model):
    mbid = models.CharField(db_index=True, max_length=36, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=500)

    release_date = models.DateField(blank=True, null=True)
    cover = models.CharField(max_length=100, null=True)
    tags = models.JSONField(null=True)

    TYPE_CHOICES = (
        ("LP", "LP"),
        ("EP", "EP"),
        ("UK", "Unknown"),
    )
    album_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="LP")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, "title")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=200, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()
    lyrics = models.TextField()

    def __str__(self):
        return f"{self.track_number}. {self.title} ({self.album.title})"


class Artist(models.Model):
    mbid = models.CharField(db_index=True, max_length=36, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    albums = models.ManyToManyField(Album, related_name="artists", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, "name")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
