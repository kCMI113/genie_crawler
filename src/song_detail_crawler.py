from selenium import webdriver
from src.song_detail.song_info_crawler import crawlSongInfo
from src.song_detail.song_daliy_chart_crawler import crawlSongDailyChart
from src.song_detail.song_lyrics_crawler import crawlSongLyrics


def crawlSongDetail(song_id: int, song_detail_url: str) -> dict:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=op)

    url = f"{song_detail_url}{song_id}"
    driver.get(url=url)

    info_data = crawlSongInfo(driver)
    listener_cnt, play_cnt = crawlSongDailyChart(driver)
    lyrics = crawlSongLyrics(driver)

    driver.close()

    info_data_upper_key = {key.upper(): item for key, item in info_data.items()}
    return {**info_data_upper_key, "LYRICS": lyrics, "LISTENER_CNT": listener_cnt, "PLAY_CNT": play_cnt}
