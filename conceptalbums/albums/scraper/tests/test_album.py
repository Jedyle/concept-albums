import pytest
import datetime
from ..parse_album import ParseAlbum


@pytest.mark.api
def test_album():
    album = ParseAlbum("3dc9ee80-0768-490d-9e43-534796da3076")
    album.load()
    assert album.as_dict() == {
        "title": "Reflektor",
        "mbid": "3dc9ee80-0768-490d-9e43-534796da3076",
        "artists": [
            {"name": "Arcade Fire", "mbid": "52074ba6-e495-4ef3-9bb4-0703888a9f68"}
        ],
        "release_date": datetime.date(2013, 10, 25),
        "cover": "https://coverartarchive.org/release/22332698-146d-436f-84c5-3b9b98a469f1/22257182085-500.jpg",
        "album_type": "LP",
        "tracks": [
            {"title": "Reflektor", "duration": "7:33"},
            {"title": "We Exist", "duration": "5:44"},
            {"title": "Flashbulb Eyes", "duration": "2:42"},
            {"title": "Here Comes the Night Time", "duration": "6:30"},
            {"title": "Normal Person", "duration": "4:22"},
            {"title": "You Already Know", "duration": "3:59"},
            {"title": "Joan of Arc", "duration": "5:26"},
            {"title": "Here Comes the Night Time II", "duration": "2:52"},
            {"title": "Awful Sound (Oh Eurydice)", "duration": "6:13"},
            {"title": "It’s Never Over (Hey Orpheus)", "duration": "6:42"},
            {"title": "Porno", "duration": "6:02"},
            {"title": "Afterlife", "duration": "5:52"},
            {"title": "Supersymmetry", "duration": "11:16"},
        ],
        "tags": [
            "indie rock",
            "rock",
            "alternative dance",
            "alternative rock",
            "art pop",
            "00s",
            "pop/rock",
        ],
    }, album.as_dict()
