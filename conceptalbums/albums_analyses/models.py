from django.conf import settings
from django.db import models
from conceptalbums.utils import JSONSchemaValidator


class AlbumAnalysis(models.Model):
    album = models.ForeignKey("albums.Album", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _analysis_schema = {
        "type": "object",
        "properties": {
            "global": {
                "description": "The text for the album global analysis",
                "type": "string",
            },
            "tracks": {
                "description": "Analyses for each (or some) tracks",
                "type": "object",
                "patternProperties": {
                    r"^\d+": {
                        "type": "object",
                        "properties": {"analysis": {"type": "string"}},
                        "additionalProperties": False,
                    }
                },
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    }

    analysis = models.JSONField(
        null=False,
        validators=[JSONSchemaValidator(schema=_analysis_schema)],
    )

    class Meta:
        unique_together = [("album", "user")]
        verbose_name_plural = "Album Analyses"
        ordering = ["created_at"]

    def __str__(self):
        return f"Analysis of {self.album} - by {self.user.username}"


class LikeAnalysis(models.Model):
    """
    When a user likes an analysis, it creates this relationship
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    analysis = models.ForeignKey(
        AlbumAnalysis, on_delete=models.CASCADE, related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "analysis")]
