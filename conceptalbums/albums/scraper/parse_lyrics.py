import requests

from django.conf import settings
from bs4 import BeautifulSoup

GENIUS_API = "https://api.genius.com"
GENIUS_URL = "https://genius.com"


class GeniusClient:
    def __init__(self):
        self.access_token = settings.GENIUS_ACCESS_KEY

    def make_api_request(self, url, method="GET"):
        return getattr(requests, method.lower())(
            GENIUS_API + url, headers={"Authorization": f"Bearer {self.access_token}"}
        )

    def find_song(self, artist_name, song_name):
        try:
            response = self.make_api_request(f"/search?q={artist_name} {song_name}")
            json_results = response.json()["response"]["hits"]
            # we fetch the first song item in the list
            song = next(hit["result"] for hit in json_results if hit["index"] == "song")
            return song
        except Exception:
            print("Song not found !")

    def get_song_lyrics_from_path(self, lyrics_path):
        lyrics_page = requests.get(GENIUS_URL + lyrics_path).content
        soup = BeautifulSoup(lyrics_page, "html.parser")
        lyrics_divs = soup.find("div", id="application").select(
            "[data-lyrics-container=true]"
        )
        for div in lyrics_divs:
            for br in div.find_all("br"):
                br.replace_with("\n")

        lyrics_divs_as_text = [el.get_text(separator="\n") for el in lyrics_divs]
        lyrics_text_flattened = "\n".join(lyrics_divs_as_text)
        return lyrics_text_flattened

    def get_song_lyrics(self, artist_name, song_name):
        song = self.find_song(artist_name, song_name)
        return self.get_song_lyrics_from_path(song["path"])
