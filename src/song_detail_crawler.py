from logging import Logger
from selenium import webdriver
from src.song_detail.song_info_crawler import crawlSongInfo
from src.song_detail.song_daliy_chart_crawler import crawlSongDailyChart
from src.song_detail.song_lyrics_crawler import crawlSongLyrics
import textwrap


def crawlSongDetail(song_id: int, song_detail_url: str, log: Logger) -> dict:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=op)

    url = f"{song_detail_url}{song_id}"
    driver.get(url=url)

    log.info("- Crawling Song Detail : %d", song_id)
    info_data = crawlSongInfo(driver)
    log.info("info data : %s", str(info_data))
    listener_cnt, play_cnt = crawlSongDailyChart(driver)
    log.info("listener_cnt, play_cnt : %d, %d", listener_cnt, play_cnt)
    lyrics = crawlSongLyrics(driver)
    log.info("lyrics : %s", textwrap.shorten(lyrics, width=50, placeholder="...") if lyrics else lyrics)

    driver.close()

    info_data_upper_key = {key.upper(): item for key, item in info_data.items()}
    return {**info_data_upper_key, "SONG_ID": song_id, "LYRICS": lyrics, "LISTENER_CNT": listener_cnt, "PLAY_CNT": play_cnt}
