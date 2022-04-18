from django.db import models
from conceptalbums.utils import unique_slug_generator


class Album(models.Model):
    mbid = models.CharField(db_index=True, max_length=36, unique=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=500)

    release_date = models.DateField(blank=True, null=True)
    cover = models.CharField(max_length=100, null=True)
    tags = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    TYPE_CHOICES = (
        ("LP", "LP"),
        ("EP", "EP"),
        ("UK", "Unknown"),
    )
    album_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="LP")

    class Meta:
        ordering = ["pk"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, "title")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=200, null=False)
    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()
    lyrics = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.track_number}. {self.title} ({self.album.title})"


class Artist(models.Model):
    mbid = models.CharField(db_index=True, max_length=36, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    albums = models.ManyToManyField(Album, related_name="artists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, "name")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
