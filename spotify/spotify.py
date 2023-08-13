import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .utils import check_substring, check_string
from config.config import DBConfig
from datetime import date


def get_spotify_url(title: str, artist: str, release_date: date) -> str | None:
    config = DBConfig()
    cid = config.spotify_cid
    secret = config.spotify_pwd
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language="ko")

    seary_query = title + " " + artist
    result = sp.search(seary_query, limit=4, type="track")
    res_score = -1
    url = ""

    for item in result["tracks"]["items"]:
        try:
            res_release_date = item["album"]["release_date"]
            res_artist_name = item["artists"][0]["name"]
            res_title = item["name"]
            res_url = item["preview_url"]
        except TypeError:
            pass

        if not res_url:
            continue

        now_score = (
            check_string(res_title, title) / 2
            + check_substring(res_title, title)
            + check_substring(res_artist_name, artist)
            + (res_release_date == release_date)
        )

        if now_score > res_score:
            url = res_url
            res_score = now_score

    if res_score <= 2:
        url = None

    try:
        if (not url) and (result["tracks"]["items"][0]["album"]["release_date"] == release_date):
            url = result["tracks"]["items"][0]["preview_url"]
    except IndexError:
        pass

    return url
