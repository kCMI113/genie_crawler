from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SONG_LYRICS_SELECTOR = "pre#pLyrics > p"


def parseSongLyrics(song_lyrics_el: WebElement) -> str:
    return song_lyrics_el.get_attribute("textContent")


def crawlSongLyrics(driver: webdriver.Chrome) -> str:
    song_lyrics_el = driver.find_element(By.CSS_SELECTOR, SONG_LYRICS_SELECTOR)
    lyrics = parseSongLyrics(song_lyrics_el)

    return lyrics
