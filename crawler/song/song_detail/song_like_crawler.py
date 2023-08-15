from bs4 import BeautifulSoup
from ...src.utils import txt2int

SONG_LIKE_SELECTOR = "a.like em#emLikeCount"


def crawlSongLike(soup: BeautifulSoup) -> int:
    song_like_el = soup.select_one(SONG_LIKE_SELECTOR)

    return txt2int(song_like_el.text)
