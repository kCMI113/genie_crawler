from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

SONG_LYRICS_SELECTOR = "pre#pLyrics > p"


def parseSongLyrics(song_lyrics_el: WebElement) -> str:
    return song_lyrics_el.get_attribute("textContent")


def crawlSongLyrics(driver: webdriver.Chrome) -> str | None:
    try:
        song_lyrics_el = driver.find_element(By.CSS_SELECTOR, SONG_LYRICS_SELECTOR)
    except NoSuchElementException as e:
        return None

    lyrics = parseSongLyrics(song_lyrics_el)

    return lyrics
