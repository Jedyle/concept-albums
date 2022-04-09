import requests
import datetime

from functools import cached_property
from bs4 import BeautifulSoup

from .constants import PROTOCOL, MUSICBRAINZ_URL, ALBUM_CATEGORY, COVER_URL


class ParseCover:
    def __init__(
        self, album_id, protocol=PROTOCOL, album_folder=ALBUM_CATEGORY, url=COVER_URL
    ):
        self.album_id = album_id
        self.url = protocol + url + album_folder

    def load(self):
        req = requests.get(self.url + self.album_id)
        if req.status_code == 200:
            self.cover = req.json()
        return req.status_code == 200

    def get_cover_small(self):
        try:
            images = self.cover["images"]
            for image in images:
                if image["front"] is True:
                    url = image["thumbnails"]["small"].split("/")
                    return url[-2] + "/" + url[-1]
        except Exception:
            pass
        return ""

    def get_cover_large(self):
        try:
            images = self.cover["images"]
            for image in images:
                if image["front"] is True:
                    url = image["thumbnails"]["large"].split("/")
                    return url[-2] + "/" + url[-1]
        except Exception:
            pass
        return ""


class ParseTrackList:

    def __init__(self, url):
        self.url = url

    def load(self):
        req = requests.get(self.url)
        if req.status_code == 200:
            page = req.content
            self.soup = BeautifulSoup(page, "html.parser")
        return req.status_code == 200

    def get_track_list(self):
        tables = self.soup.find_all("table", {"class": "tbl"})
        lists = []
        for table in tables:
            try:
                subh = table.tbody.find("tr", {"class": "subh"}).find_all("th")
                title_index = 0
                duration_index = 0
                for i in range(len(subh)):
                    if subh[i].text == "Title":
                        title_index = i
                    if subh[i].text == "Length":
                        duration_index = i

                tracks = table.tbody.find_all("tr")[1:]
                cd = []
                for track in tracks:
                    try:
                        cols = track.find_all("td")
                        title = cols[title_index].a.text
                        cd.append(
                            {
                                "title": title,
                                "duration": cols[duration_index].text,
                            }
                        )
                    except IndexError:
                        pass
                name = table.find_all("span", {"class": "medium-name"})
                if name:
                    title = name[0].text
                else:
                    title = ""
                lists.append(
                    {
                        "medium_title": title,
                        "tracks": cd,
                    }
                )
            except Exception:
                pass
        return lists


class ParseAlbum:
    def __init__(
        self,
        album_id,
        protocol=PROTOCOL,
        url=MUSICBRAINZ_URL,
        album_folder=ALBUM_CATEGORY,
    ):
        self.album_id = album_id
        self.root_url = protocol + url
        self.url = protocol + url + album_folder

    def load(self):
        req = requests.get(self.url + self.album_id)
        if req.status_code == 200:
            page = req.content
            self.soup = BeautifulSoup(page, "html.parser")
        return req.status_code == 200

    def as_dict(self):
        return {
            "title": self.title,
            "mbid": self.album_id,
            "artists": self.artists,
            "release_date": self.release_date,
            "cover": self.cover,
            "album_type": self.album_type,
            "tracks": self.track_list,
            "tags": self.tags,
        }

    @cached_property
    def cover(self):
        parse_cover = ParseCover(self.album_id)
        if parse_cover.load():
            return parse_cover.get_cover_large()

    @cached_property
    def title(self):
        div = self.soup.find("div", {"class": "rgheader"})
        return div.a.text

    @cached_property
    def artists(self):
        links = self.soup.find("p", {"class": "subheader"}).find_all("a")
        artists = []
        for link in links:
            artist = {"name": link.text, "mbid": link["href"].split("/")[-1]}
            artists.append(artist)
        return artists

    @cached_property
    def release_date(self):
        table = self.soup.find("table", {"class": "tbl"})
        dates = []
        for row in table.tbody.find_all("span", {"class": "release-date"}):
            try:
                r_date = row.text
                if len(r_date) == 4:
                    r_date = r_date + "-12-31"
                try:
                    date = datetime.datetime.strptime(r_date, "%Y-%m-%d").date()
                    dates.append(date)
                except ValueError:
                    pass
            except IndexError:
                pass
        if dates:
            return min(dates)
        else:
            return None

    @cached_property
    def track_list(self):
        table = self.soup.find("table", {"class": "tbl"})
        first_release = table.tbody.find_all("tr")[1:2]
        if first_release:
            release_link = first_release[0].find_all("td")[0].find_all("a")[-1]["href"].lstrip("/")
            parse_track_list = ParseTrackList(self.root_url + release_link)
            if parse_track_list.load():
                return parse_track_list.get_track_list()

    @cached_property
    def album_type(self):
        album_type = self.soup.find("dl", {"class": "properties"}).find(
            "dd", {"class": "type"}
        )
        if album_type:
            album_type = album_type.text
            return {"Album": "LP", "EP": "EP"}.get(album_type, "UK")
        return "UK"

    @cached_property
    def tags(self):
        tag_list = self.soup.find("div", {"id": "sidebar-tags"})
        if tag_list:
            tags = tag_list.find_all("a")
            tag_names = [
                tag.text for tag in tags if tag.get("href", "").startswith("/tag")
            ]
            return tag_names
        else:
            return []
