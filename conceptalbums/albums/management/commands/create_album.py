from django.core.management.base import BaseCommand

from albums.commands import create_album_from_musicbrainz_and_genius


class Command(BaseCommand):
    help = "Create an album from a mbid, also fetching tracks and lyrics"

    def add_arguments(self, parser):
        parser.add_argument("mbid", nargs="+", type=str)

    def handle(self, *args, **options):
        mbids = options["mbid"]
        for mbid in mbids:
            create_album_from_musicbrainz_and_genius(mbid)
            self.stdout.write(self.style.SUCCESS(f"Album {mbid} created !"))
