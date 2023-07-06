from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from logging import Logger
from src.utils import resizeImg
from omegaconf import DictConfig


def crawlAlbumInfo(album_id: int, album_detail_url: str, log: Logger, config: DictConfig) -> dict:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=op)

    url = f"{album_detail_url}{album_id}"
    driver.get(url=url)

    log.info("- Crawling Album Release Date : %d", album_id)

    album_detail_info = driver.find_element(By.CLASS_NAME, "album-detail-infos")

    info_zone = album_detail_info.find_element(By.CLASS_NAME, "info-zone")
    date_info = info_zone.find_elements(By.TAG_NAME, "li")[-1].text
    date_info = list(map(int, date_info.split(".")))
    date_info = date(date_info[0], date_info[1], date_info[2])

    photo_zone = album_detail_info.find_element(By.CLASS_NAME, "photo-zone")
    img = (photo_zone.find_element(By.CLASS_NAME, "thum")).find_element(By.TAG_NAME, "a")
    img_path = img.get_attribute("href")
    resized_img_path = resizeImg(img_path[: img_path.find("/dims")], config.img_resize, config.max_resize)

    driver.close()

    log.info("RELEASE_DATE: %s", date_info.strftime("%Y-%m-%d"))
    log.info("ALBUM_IMG_PATH: %s", resized_img_path)

    return {"ALBUM_ID": album_id, "RELEASE_DATE": date_info, "ALBUM_IMG_PATH": resized_img_path}
