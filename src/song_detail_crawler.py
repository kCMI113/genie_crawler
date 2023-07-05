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
    daily_chart = crawlSongDailyChart(driver)
    lyrics = crawlSongLyrics(driver)

    driver.close()

    return {"info_data": info_data, "lyrics": lyrics, **daily_chart}
