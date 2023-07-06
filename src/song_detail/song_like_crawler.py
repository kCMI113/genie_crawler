from bs4 import BeautifulSoup, Tag

SONG_LIKE_SELECTOR = "a.like em#emLikeCount"


def crawlSongLike(soup: BeautifulSoup) -> int:
    song_like_el = soup.select_one(SONG_LIKE_SELECTOR)
    song_like = int(song_like_el.text)

    return song_like
