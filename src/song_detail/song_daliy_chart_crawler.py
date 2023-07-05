from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SONG_DAILY_CHART_SELECTOR = ".daily-chart div.total"
SONG_DAILY_CHART_LISTENER_CNT_SELECTOR = "div:nth-child(1) p"
SONG_DAILY_CHART_PLAY_CNT_SELECTOR = "div:nth-child(2) p"


def parseListenerCnt(listener_cnt_el: WebElement) -> int:
    return int(listener_cnt_el.text.replace(",", ""))


def parsePlayCnt(play_cnt_el: WebElement) -> int:
    return int(play_cnt_el.text.replace(",", ""))


def crawlSongDailyChart(driver: webdriver.Chrome) -> dict:
    song_daliy_chart_el = driver.find_element(By.CSS_SELECTOR, SONG_DAILY_CHART_SELECTOR)

    # listener cnt
    listener_cnt_el = song_daliy_chart_el.find_element(By.CSS_SELECTOR, SONG_DAILY_CHART_LISTENER_CNT_SELECTOR)
    listener_cnt = parseListenerCnt(listener_cnt_el)

    # play cnt
    play_cnt_el = song_daliy_chart_el.find_element(By.CSS_SELECTOR, SONG_DAILY_CHART_PLAY_CNT_SELECTOR)
    play_cnt = parsePlayCnt(play_cnt_el)

    return {"listener_cnt": listener_cnt, "play_cnt": play_cnt}
