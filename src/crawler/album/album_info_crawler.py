from datetime import date
from logging import Logger
from bs4 import BeautifulSoup
import requests

from ..utils import resizeImg


def crawlAlbumInfo(album_id: int, config, album_detail_url: str, log: Logger) -> dict:
    url = f"{album_detail_url}{album_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    log.info("- Crawling Album Release Date : %d", album_id)

    album_detail_info = soup.select_one(".album-detail-infos")

    info_zone = album_detail_info.select_one(".info-zone")
    date_info = info_zone.select("li")[-1].text
    date_info = list(map(int, date_info.split(".")))
    date_info = date(date_info[0], date_info[1], date_info[2])
    log.info("RELEASE_DATE: %s", date_info.strftime("%Y-%m-%d"))

    """
    photo_zone = album_detail_info.select_one(".photo-zone")
    cover = photo_zone.select_one(".cover")
    img_path = cover.find("img")["src"]
    resized_img_path = "https:" + resizeImg(img_path[: img_path.find("/dims")], config.img_resize, config.max_resize)
    log.info("ALBUM_IMG_PATH: %s", resized_img_path)
    """

    return {"ALBUM_ID": album_id, "RELEASE_DATE": date_info}
