from bs4 import BeautifulSoup, Tag

SONG_LYRICS_SELECTOR = "pre#pLyrics > p"


def parseSongLyrics(song_lyrics_el: Tag) -> str:
    return song_lyrics_el.text


def crawlSongLyrics(driver: BeautifulSoup) -> str | None:
    song_lyrics_el = driver.select_one(SONG_LYRICS_SELECTOR)

    if not song_lyrics_el:
        return None

    lyrics = parseSongLyrics(song_lyrics_el)

    return lyrics
