from logging import Logger
from selenium import webdriver
from song_detail.song_create_date_crawler import crawlReleaseDateInfo
import textwrap


def crawlSongDetail(song_id: int, song_detail_url: str, log: Logger) -> dict:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=op)

    url = f"{song_detail_url}{song_id}"
    driver.get(url=url)

    log.info("- Crawling Song Detail : %d", song_id)
    date_info = crawlReleaseDateInfo(driver)
    log.info("date_info: ", date_info)

    driver.close()

    return {"SONG_ID": song_id, "RELEASE_DATE": date_info}
