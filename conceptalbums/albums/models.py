from django.db import models


class Album(models.Model):

    title = models.CharField(max_length=500)
    mbid = models.CharField(db_index=True, max_length=36, null=True)
    release_date = models.DateField(blank=True, null=True)
    cover = models.CharField(max_length=100, null=True)

    TYPE_CHOICES = (
        ("LP", "LP"),
        ("EP", "EP"),
        ("UK", "Unknown"),
    )

    album_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="LP")

    def __str__(self):
        return self.title


class Track(models.Model):
    name = models.CharField(max_length = 200, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()
    lyrics = models.TextField()

    def __str__(self):
        return f"{self.track_number}. {self.name} ({self.album.title})"


class Artist(models.Model):
    mbid = models.CharField(
        db_index=True,
        max_length=36,
        null=True
    )
    name = models.CharField(max_length=100)
    albums = models.ManyToManyField(Album, related_name="artists", blank=True)
    photo = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


