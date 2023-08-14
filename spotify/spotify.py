import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .utils import check_substring, check_string
from config.config import DBConfig
from datetime import date

config = DBConfig()
cid = config.spotify_cid
secret = config.spotify_pwd
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language="ko")


def calculateValidScore(item, title, artist, release_date) -> (int, str):
    try:
        res_release_date = item["album"]["release_date"]
        res_artist_name = item["artists"][0]["name"]
        res_title = item["name"]
        res_url = item["preview_url"]

        score = (
        check_string(res_title, title) / 2
        + check_substring(res_title, title)
        + check_substring(res_artist_name, artist)
        + (res_release_date == release_date)
        )
        return score, res_url
    
    except TypeError:
        return -1, None


def checkReleaseDate(item, release_date) -> str | None:
    try:
        if item["album"]["release_date"] == release_date:
            return item["preview_url"]
    except IndexError:
        pass


def getSpotifyUrl(title: str, artist: str, release_date: date) -> str | None:
    search_query = title + " " + artist
    result = sp.search(search_query, limit=4, type="track")
    res_score = -1
    standard_score = 2
    url = ""

    for item in result["tracks"]["items"]:
        now_score, now_url = calculateValidScore(item, title, artist, release_date)

        if now_score > res_score:
            # Update max score and URL
            url = now_url
            res_score = now_score

    # If the maximum score is less than the standard, it is discarded
    if res_score <= standard_score:
        url = None

    # If url is None, recheck first in search results with release date
    if not url and len(result["tracks"]["items"])>0:
        return checkReleaseDate(result["tracks"]["items"][0], release_date)

    return url
